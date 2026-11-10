"""S0 입력 준비: EY 엑셀 4개 시트를 config/*.json으로 옮기고 전월과 달라진 점을 config_diff.md로 남긴다."""
import glob
import html
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path

from common import REPO_ROOT, ConfigError, RunPaths, get_logger, load_config, new_parser, outputs_ready, sha256_file

GENERATED = ("targets", "brands", "search_terms", "keywords")


def clean(value):
    return value.strip() if isinstance(value, str) else value


def find_workbook(s0_input):
    # pathlib.glob은 폴더 이름의 한글 조합 방식(NFC/NFD)이 다르면 못 찾는다. glob.glob은 고정 경로를 그대로 쓴다.
    matches = sorted(glob.glob(str(REPO_ROOT / s0_input["excel_glob"])))
    if len(matches) != 1:
        raise ConfigError(f"엑셀은 정확히 1개여야 합니다({s0_input['excel_glob']}): {matches}")
    return Path(matches[0])


def load_sheets(path, s0_input):
    import openpyxl

    workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
    sheets = {}
    for key, spec in s0_input["sheets"].items():
        if spec["name"] not in workbook.sheetnames:
            raise ConfigError(f"시트가 없습니다: {spec['name']}")
        sheets[key] = [list(row) for row in workbook[spec["name"]].iter_rows(values_only=True)]
    workbook.close()
    return sheets


def data_rows(rows, spec):
    """머리글을 검사한 뒤 (엑셀 행번호, {열 이름: 값})을 돌려준다. 머리글이 다르면 멈춘다."""
    header = rows[spec["header_row"] - 1]
    for name, (index, expected) in spec["columns"].items():
        actual = header[index] if index < len(header) else None
        if clean(actual) != expected:
            raise ConfigError(f"시트 '{spec['name']}' {name} 열 머리글이 바뀌었습니다: {actual!r} (기대값 {expected!r})")
    for number, row in enumerate(rows[spec["header_row"]:], start=spec["header_row"] + 1):
        yield number, {name: (row[index] if index < len(row) else None) for name, (index, _) in spec["columns"].items()}


def country_name(value, s0_input):
    value = clean(value) or ""
    return s0_input["country_alias"].get(value, value)


def read_console_targets(s0_input):
    path = Path(s0_input["console_fixed_targets"]).expanduser()
    if not path.exists():
        raise ConfigError(f"콘솔 대상 파일이 없습니다: {path}")
    return json.loads(path.read_text(encoding="utf-8"))["targets"]


def build_targets(rows, s0_input, search_urls):
    spec = s0_input["sheets"]["targets"]
    names, targets, total = s0_input["retailer_names"], [], None
    for _, row in data_rows(rows, spec):
        region = clean(row["region"])
        if isinstance(region, str) and region.startswith(spec["total_marker"]):
            total = row
            break
        if not region:
            continue
        country, sheet_name = country_name(row["country"], s0_input), clean(row["retailer"])
        if f"{country}|{sheet_name}" not in names:
            raise ConfigError(f"이름 표에 없는 리테일러입니다: {country}|{sheet_name}")
        if row["osm"] not in ("O", "X"):
            raise ConfigError(f"OSM 보유 값이 O/X가 아닙니다: {country}|{sheet_name}={row['osm']!r}")
        retailer = names[f"{country}|{sheet_name}"]
        osm = row["osm"] == "O"
        zyte = search_urls.get(f"{country}|{retailer}", {})
        if not osm and not zyte:
            raise ConfigError(f"검색 수집 대상인데 search_urls에 없습니다: {country}|{retailer}")
        targets.append({
            "country": country, "retailer": retailer, "sheet_retailer": sheet_name,
            "region": region, "subsidiary": clean(row["subsidiary"]), "osm": osm, "flow": "OSM" if osm else "검색",
            "console_country_codes": s0_input["console_country_codes"].get(country) if osm else None,
            "zyte_geolocation": zyte.get("zyte_geolocation"), "zyte_geolocation_group": zyte.get("zyte_geolocation_group"),
            "zyte_tier": zyte.get("zyte_tier"), "search_method": zyte.get("search_method"),
        })
    if total is None:
        raise ConfigError("대상 시트에서 합계 줄을 찾지 못했습니다")
    osm_count = sum(t["osm"] for t in targets)
    if (len(targets), osm_count) != (total["retailer"], total["osm"]):
        raise ConfigError(f"대상 건수가 시트 합계와 다릅니다: 읽음 {len(targets)}/{osm_count}, 합계 {total['retailer']}/{total['osm']}")
    return targets


def check_console(targets, s0_input):
    """OSM 대상이 콘솔 고정 대상과 같은지 확인한다. 다르면 S1a 결과가 어긋나므로 멈춘다."""
    console = {(s0_input["country_alias"].get(t["country"], t["country"]), t["retailer"]) for t in read_console_targets(s0_input)}
    ours = {(t["country"], t["retailer"]) for t in targets if t["osm"]}
    if console != ours:
        raise ConfigError(f"콘솔 대상과 다릅니다. 시트에만: {sorted(ours - console)}, 콘솔에만: {sorted(console - ours)}")


def build_brands(rows, s0_input):
    spec = s0_input["sheets"]["brands"]
    brands = defaultdict(lambda: defaultdict(set))
    for number, row in data_rows(rows, spec):
        values = [row[name] for name in ("region", "country", "category", "brand")]
        filled = [value for value in values if value not in (None, "")]
        if not filled:
            continue
        if len(filled) != 4:
            raise ConfigError(f"경쟁브랜드 {number}행은 4칸이 다 차 있어야 합니다: {values}")
        brands[country_name(row["country"], s0_input)][clean(row["category"])].add(clean(row["brand"]).upper())
    for country, categories in s0_input["brand_overrides"].items():
        if not country.startswith("_"):
            for category, values in categories.items():
                brands[country][category] = set(values)
    return {country: {category: sorted(values) for category, values in sorted(categories.items())} for country, categories in sorted(brands.items())}


def build_search_terms(rows, s0_input, targets):
    spec = s0_input["sheets"]["search_terms"]
    allowed = {(t["country"], t["retailer"]) for t in targets if not t["osm"]}
    terms, excluded, seen = [], [], set()
    for number, row in data_rows(rows, spec):
        if clean(row["osm"]) != spec["use_osm_value"]:
            continue
        retailer, country = clean(row["retailer"]), country_name(row["country"], s0_input)
        if (country, retailer) not in allowed:
            raise ConfigError(f"Search Term {number}행의 리테일러가 검색 수집 대상에 없습니다: {country}|{retailer}")
        if row["keyword"] in (None, ""):
            raise ConfigError(f"Search Term {number}행의 J열 검색어가 비어 있습니다")
        seen.add((country, retailer))
        item = {"excel_row": number, "country": country, "retailer": retailer, "category": clean(row["category"]),
                "english": row["english"], "keyword": str(row["keyword"]),
                "ey_proposal": row["ey_proposal"], "source_note": row["source_note"]}
        (excluded if clean(item["keyword"]) == spec["excluded_keyword_marker"] else terms).append(item)
    if seen != allowed:
        raise ConfigError(f"검색어가 하나도 없는 검색 수집 대상이 있습니다: {sorted(allowed - seen)}")
    return {"terms": terms, "excluded": excluded}


def build_keywords(rows, s0_input):
    spec = s0_input["sheets"]["keywords"]
    keywords = defaultdict(list)
    for _, row in data_rows(rows, spec):
        if row["country"] and row["type"] and row["keyword"]:
            keywords[country_name(row["country"], s0_input)].append({"type": row["type"], "keyword": html.unescape(str(row["keyword"])).strip().lower()})
    return dict(sorted(keywords.items()))


def write_json(path, data):
    descriptor, temp_name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=1)
            handle.write("\n")
        os.chmod(temp_name, 0o644)
        os.replace(temp_name, path)
    except BaseException:
        os.unlink(temp_name)
        raise


def previous_month(month):
    year, number = map(int, month.split("-"))
    return f"{year - 1}-12" if number == 1 else f"{year}-{number - 1:02d}"


def compare_map(title, before, after):
    """키별 값이 달라진 곳을 마크다운 표 줄로 만든다."""
    lines = []
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key), after.get(key)
        if old != new:
            lines.append(f"| {title} | {key} | {old} | {new} |")
    return lines


def comparable(name, data):
    """파일별로 비교할 값만 키-값으로 펼친다. 생성 정보 등은 뺀다."""
    if name == "targets":
        return {f"{t['country']}|{t['retailer']}": t["flow"] for t in data["targets"]}
    if name == "brands":
        return {f"{c}|{cat}": values for c, cats in data["brands"].items() for cat, values in cats.items()}
    if name == "keywords":
        return {c: [(k["type"], k["keyword"]) for k in items] for c, items in data["keywords"].items()}
    terms = {f"{t['excel_row']}": (t["country"], t["retailer"], t["category"], t["keyword"]) for t in data["terms"]}
    terms.update({f"{t['excel_row']}(제외)": (t["country"], t["retailer"], t["category"]) for t in data["excluded"]})
    return terms


def render_diff(month, previous, current, loaded_previous):
    header = [f"# S0 설정 변경 확인 ({previous} → {month})", ""]
    if not loaded_previous:
        return "\n".join(header + [f"전월 설정(runs/{previous}/config)이 없어 비교하지 않았습니다.", ""])
    lines = []
    for name in GENERATED:
        lines += compare_map(name, comparable(name, loaded_previous[name]), comparable(name, current[name]))
    summary = [f"- {name}: 전월 {len(comparable(name, loaded_previous[name]))}개 키, 이번 달 {len(comparable(name, current[name]))}개 키" for name in GENERATED]
    if not lines:
        return "\n".join(header + summary + ["", "달라진 값 없음.", ""])
    return "\n".join(header + summary + ["", f"달라진 값 {len(lines)}개. EY 메일·두레이 근거가 있는 변경인지 확인하세요.", "", "| 파일 | 키 | 전월 | 이번 달 |", "| --- | --- | --- | --- |"] + lines + [""])


def build_all(sheets, s0_input, search_urls, source):
    targets = build_targets(sheets["targets"], s0_input, search_urls)
    check_console(targets, s0_input)
    search_terms = build_search_terms(sheets["search_terms"], s0_input, targets)
    return {
        "targets": {"_source": source, "targets": targets},
        "brands": {"_source": source, "category_fallback": s0_input["category_fallback"], "brands": build_brands(sheets["brands"], s0_input)},
        "search_terms": {"_source": source, **search_terms},
        "keywords": {"_source": source, "keywords": build_keywords(sheets["keywords"], s0_input)},
    }


def load_previous(month, root):
    run = RunPaths(previous_month(month), root)
    if not all((run.sub("config") / f"{name}.json").exists() for name in GENERATED):
        return None
    return {name: load_config(run, name) for name in GENERATED}


def main(argv):
    args = new_parser("S0 입력 준비: EY 엑셀 → config/*.json").parse_args(argv)
    run = RunPaths(args.month).create()
    logger = get_logger(run, "s0")
    outputs = [run.sub("config") / f"{name}.json" for name in GENERATED] + [run.sub("config") / "config_diff.md"]
    if outputs_ready(outputs, args.force):
        logger.info("출력이 이미 있어 건너뜁니다(다시 만들려면 --force)")
        return 0
    s0_input = load_config(run, "s0_input")
    workbook = find_workbook(s0_input)
    source = {"excel": str(workbook.relative_to(REPO_ROOT)), "sha256": sha256_file(workbook)}
    logger.info("엑셀 읽기: %s", source["excel"])
    current = build_all(load_sheets(workbook, s0_input), s0_input, load_config(run, "search_urls")["retailers"], source)
    for name, data in current.items():
        write_json(run.sub("config") / f"{name}.json", data)
    diff = render_diff(run.month, previous_month(run.month), current, load_previous(run.month, run.root))
    (run.sub("config") / "config_diff.md").write_text(diff, encoding="utf-8")
    logger.info("대상 %d곳(OSM %d·검색 %d), 브랜드 %d개국, 검색어 %d개(제외 표시 %d개), 리리부 %d개국",
                len(current["targets"]["targets"]), sum(t["osm"] for t in current["targets"]["targets"]),
                sum(not t["osm"] for t in current["targets"]["targets"]), len(current["brands"]["brands"]),
                len(current["search_terms"]["terms"]), len(current["search_terms"]["excluded"]), len(current["keywords"]["keywords"]))
    return 0
