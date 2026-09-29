"""Extract UTF-8 constants from ELF .rodata without executing library code.

These constants are evidence of included strings, not recovered source or a
proof of runtime control flow. Output offsets refer to the original ELF file.
"""
import argparse
import json
import struct
from pathlib import Path


def strings(path):
    raw = path.read_bytes()
    if raw[:6] != b"\x7fELF\x02\x01":
        raise ValueError("Expected ELF64 little-endian")
    shoff = struct.unpack_from("<Q", raw, 40)[0]
    shsize, shnum, shstrndx = struct.unpack_from("<HHH", raw, 58)
    sections = [struct.unpack_from("<IIQQQQIIQQ", raw, shoff + i * shsize) for i in range(shnum)]
    names = sections[shstrndx]
    names = raw[names[4]:names[4] + names[5]]
    for section in sections:
        name = names[section[0]:].split(b"\0", 1)[0]
        if name != b".rodata":
            continue
        offset = section[4]
        for chunk in raw[offset:offset + section[5]].split(b"\0"):
            try:
                text = chunk.decode("utf-8")
            except UnicodeDecodeError:
                text = ""
            if len(text) >= 4 and all(c.isprintable() or c in "\n\r\t" for c in text):
                yield {"offset": hex(offset), "text": text}
            offset += len(chunk) + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = []
    for source in sorted(args.root.rglob("*.so")):
        relative = source.relative_to(args.root)
        dest = args.output / relative.with_suffix(".strings.jsonl")
        dest.parent.mkdir(parents=True, exist_ok=True)
        values = list(strings(source))
        dest.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in values))
        manifest.append({"source": str(relative), "output": str(dest), "strings": len(values)})
    (args.output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Extracted .rodata constants from {len(manifest)} libraries; did not run them.")


if __name__ == "__main__":
    main()
