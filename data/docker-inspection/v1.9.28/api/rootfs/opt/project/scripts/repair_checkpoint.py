# 실행 스텁 — 구현은 같은 폴더의 컴파일된 확장 모듈(repair_checkpoint.*.so). 소스는 CNX 보관.
# `python repair_checkpoint.py …` 로 실행하면 확장 모듈의 CLI 가 돌고, 모듈로 임포트되면 확장 모듈의 이름공간을 그대로 노출한다.
import glob as _g, importlib.util as _u, os as _os, sys as _sys
if __name__ == "__main__":
    _os.environ["CLINIC_ENTRY"] = "repair_checkpoint"
_so = _g.glob(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "repair_checkpoint.*.so"))[0]
_m = _sys.modules.get("repair_checkpoint")
if _m is None or getattr(_m, "__file__", "") != _so:
    _spec = _u.spec_from_file_location("repair_checkpoint", _so)
    _m = _u.module_from_spec(_spec)
    _sys.modules["repair_checkpoint"] = _m
    _spec.loader.exec_module(_m)
if __name__ != "__main__":
    # 모듈로 임포트된 경우(테스트의 spec_from_file_location 등): 이 스텁을 확장 모듈의 프록시로 바꿔
    # 속성 읽기·쓰기(monkeypatch 포함)를 전부 확장 모듈로 전달한다.
    import gc as _gc, types as _t

    class _Proxy(_t.ModuleType):
        def __getattr__(self, k):
            return getattr(_m, k)

        def __setattr__(self, k, v):
            setattr(_m, k, v)

        def __delattr__(self, k):
            delattr(_m, k)

    for _r in _gc.get_referrers(globals()):
        if isinstance(_r, _t.ModuleType) and getattr(_r, "__dict__", None) is globals():
            _r.__class__ = _Proxy
            break
