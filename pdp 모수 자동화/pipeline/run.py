"""단계 실행 입구: python pipeline/run.py <단계> [--month YYYY-MM] [--dry-run|--run]."""
import importlib
import sys

from common import RunPaths

STEPS = {"s0": "s0_config", "s1a": "s1a_osm", "s1b": "s1b_search", "s2": "s2_filter",
         "s3": "s3_pages", "s4": "s4_sellers", "s5": "s5_judge", "s6": "s6_share", "next": "make_next_version"}


def main(argv):
    if len(argv) >= 2 and argv[0] == "init":
        RunPaths(argv[1]).create()
        print(f"회차 폴더 준비됨: {RunPaths(argv[1]).directory}")
        return 0
    if not argv or argv[0] not in STEPS:
        print(f"사용법: run.py init YYYY-MM | run.py {{{','.join(STEPS)}}} [인자]")
        return 2
    try:
        module = importlib.import_module(STEPS[argv[0]])
    except ModuleNotFoundError as error:
        if error.name != STEPS[argv[0]]:
            raise
        print(f"{argv[0]} 단계는 아직 구현되지 않았습니다")
        return 2
    return module.main(argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
