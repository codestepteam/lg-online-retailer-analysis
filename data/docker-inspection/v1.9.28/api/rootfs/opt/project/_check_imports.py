# 빌드 검증용 — 컴파일된 모듈 전부 임포트 (Dockerfile.prod 가 실행 후 삭제)
import importlib, os, sys
os.environ.setdefault("CLINIC_ENTRY", "")   # 진입 가드가 켜지지 않게
for k, v in {"DB_HOST": "localhost", "DB_PORT": "3306", "DB_NAME": "lg_clinic", "DB_USER": "x", "DB_PASSWORD": "x"}.items():
    os.environ.setdefault(k, v)                # 임포트 시 설정 검증만 통과 (접속은 하지 않음)
mods = [m.strip() for m in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_modules.txt")) if m.strip()]
bad, warn = [], []
for m in mods:
    try:
        importlib.import_module(m)
    except Exception as e:  # noqa: BLE001
        if type(e).__name__ in ("OperationalError", "InterfaceError"):   # 임포트 시 DB 접속을 시도하는 스크립트 — 빌드 환경엔 DB 가 없다
            warn.append(f"{m}: {type(e).__name__} (DB 없음 — 정상)")
        else:
            bad.append(f"{m}: {type(e).__name__}: {e}")
print(f"imported {len(mods) - len(bad)}/{len(mods)} compiled modules" + (f", db-only warnings: {len(warn)}" if warn else ""))
for w in warn:
    print("  warn:", w)
if bad:
    print("\n".join(bad))
    sys.exit(1)
