"""Inspect a docker-save archive without loading or executing its image.

Copy only regular files under opt/project, opt/airflow/dags, and app.
Apply layer deletion markers to the selected files and retain provenance.
Do not follow archive symlinks or use extractall.
"""

import argparse
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath


def safe_name(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe archive path: {name}")
    return str(path)


def selected(name):
    return any(name.startswith(p) for p in ("opt/project/", "opt/airflow/dags/", "app/"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    inventory = {}
    events = []
    with tempfile.TemporaryDirectory(prefix="clinic-image-inspect-") as scratch:
        scratch = Path(scratch)
        with tarfile.open(args.archive, "r|gz") as outer:
            for member in outer:
                name = safe_name(member.name)
                if not member.isfile():
                    continue
                dest = scratch / name
                dest.parent.mkdir(parents=True, exist_ok=True)
                with outer.extractfile(member) as src, dest.open("xb") as dst:
                    shutil.copyfileobj(src, dst)
        manifest = json.loads((scratch / "manifest.json").read_text())
        if len(manifest) != 1:
            raise ValueError("Expected one image per delivery archive")
        entry = manifest[0]
        config = json.loads((scratch / safe_name(entry["Config"])).read_text())
        for index, layer in enumerate(entry["Layers"]):
            print(f"Reading layer {index + 1}/{len(entry['Layers'])}", flush=True)
            with tarfile.open(scratch / safe_name(layer), "r|*") as archive:
                for member in archive:
                    name = safe_name(member.name)
                    if not selected(name):
                        continue
                    path = PurePosixPath(name)
                    if path.name.startswith(".wh."):
                        if path.name == ".wh..wh..opq":
                            prefix = str(path.parent) + "/"
                            gone = [key for key in inventory if key.startswith(prefix)]
                        else:
                            target = str(path.parent / path.name[4:])
                            gone = [key for key in inventory if key == target or key.startswith(target + "/")]
                        for key in gone:
                            (args.output / "rootfs" / key).unlink(missing_ok=True)
                            del inventory[key]
                        events.append({"layer": index, "marker": name, "removed": gone})
                        continue
                    if not member.isfile():
                        continue
                    if member.size > 100 * 1024 * 1024:
                        events.append({"layer": index, "skipped_large_file": name, "size": member.size})
                        continue
                    dest = args.output / "rootfs" / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as src, dest.open("wb") as dst:
                        shutil.copyfileobj(src, dst)
                    inventory[name] = {"size": member.size, "layer": index, "layer_path": layer,
                                       "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}
        # Image environment can include secrets; persist variable names only.
        cfg = config.get("config", {})
        summary = {"archive": str(args.archive), "repo_tags": entry.get("RepoTags"),
                   "architecture": config.get("architecture"), "os": config.get("os"),
                   "created": config.get("created"), "working_dir": cfg.get("WorkingDir"),
                   "entrypoint": cfg.get("Entrypoint"), "cmd": cfg.get("Cmd"),
                   "env_names": [x.split("=", 1)[0] for x in cfg.get("Env", [])],
                   "layer_count": len(entry["Layers"]), "files": inventory, "events": events}
        (args.output / "inventory.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({k: v for k, v in summary.items() if k not in ("files", "events")}, ensure_ascii=False))
        print(f"Selected final regular files: {len(inventory)}")


if __name__ == "__main__":
    main()
