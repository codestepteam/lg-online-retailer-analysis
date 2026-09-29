#!/usr/bin/env python3
"""Require confirmed project decisions to be persisted before a turn ends."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DECISIONS = ROOT / "docs" / "DECISIONS.md"
CONTEXT_DOCS = (
    DECISIONS,
    ROOT / "PROJECT_CONTEXT.md",
    ROOT / "docs" / "BUSINESS_RULES.md",
    ROOT / "AGENTS.md",
)
STATE_DIR = Path(
    os.environ.get(
        "PROJECT_DECISION_HOOK_STATE_DIR",
        str(Path(tempfile.gettempdir()) / "codex-project-decision-hooks"),
    )
)

CONFIRMED_PATTERNS = (
    r"(?:하기로|쓰기로|사용하기로|도입하기로|채택하기로|전환하기로)\s*(?:했|했다|했습니다|했어|했거든|함|결정|확정)",
    r"(?:결정|확정|채택)(?:이|가|은|는)?\s*(?:됐|되었|되었습니다|됐어|된\s*거|했|했다|했습니다|함)",
    r"(?:정해졌|정했다|정했습니다|정했어)",
    r"\b(?:we|i|the team)\s+(?:have\s+)?decided\b",
    r"\b(?:decided to|adopted|has been confirmed|is confirmed)\b",
)
TENTATIVE_PATTERNS = (
    r"(?:결정|확정|채택|정)(?:할까|해야|하면|할지|해볼까)",
    r"(?:고민|검토|후보|제안|아이디어|어떨까|어때\??)",
    r"\b(?:considering|proposal|candidate|should we|might use|could use)\b",
)


def read_event() -> dict:
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return {}


def safe_id(value: object) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", str(value or "unknown"))[:160]


def state_path(turn_id: object) -> Path:
    return STATE_DIR / f"{safe_id(turn_id)}.json"


def mtime_ns(path: Path) -> int:
    try:
        return path.stat().st_mtime_ns
    except FileNotFoundError:
        return 0


def is_decision_candidate(prompt: str) -> bool:
    normalized = " ".join(prompt.split()).lower()
    confirmed = any(re.search(pattern, normalized, re.IGNORECASE) for pattern in CONFIRMED_PATTERNS)
    if not confirmed:
        return False
    tentative = any(re.search(pattern, normalized, re.IGNORECASE) for pattern in TENTATIVE_PATTERNS)
    strong = any(
        token in normalized
        for token in ("하기로 했", "결정됐", "결정되었", "확정됐", "확정되었", "채택했", "decided to")
    )
    return strong or not tentative


def save_state(event: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    prompt = str(event.get("prompt") or "")
    state = {
        "session_id": event.get("session_id"),
        "turn_id": event.get("turn_id"),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "prompt_excerpt": prompt[:800],
        "created_at_ns": time.time_ns(),
        "decision_mtime_ns": mtime_ns(DECISIONS),
        "context_mtimes_ns": {str(path.relative_to(ROOT)): mtime_ns(path) for path in CONTEXT_DOCS},
        "status": "pending",
    }
    state_path(event.get("turn_id")).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def prompt_hook(event: dict) -> int:
    prompt = str(event.get("prompt") or "")
    if not is_decision_candidate(prompt):
        return 0
    save_state(event)
    turn_id = safe_id(event.get("turn_id"))
    message = (
        "프로젝트에 영향을 주는 확정 의사결정 후보를 감지했다. 사용자 문맥을 직접 판단하라. "
        "확정된 결정이면 이 턴을 끝내기 전에 docs/DECISIONS.md에 날짜·결정·근거·영향을 기록하고, "
        "PROJECT_CONTEXT.md, docs/BUSINESS_RULES.md, AGENTS.md 중 실제로 영향받는 문서도 함께 갱신하라. "
        "질문·제안·가정이거나 프로젝트 지식에 영향이 없으면 문서를 억지로 고치지 말고 다음 명령으로 후보를 해제하라: "
        f"/usr/bin/python3 \"{Path(__file__).resolve()}\" resolve --turn-id \"{turn_id}\" "
        "--ignore --reason \"확정 결정이 아닌 이유\". 사용자 결정을 AI 추론으로 확대하지 마라."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": message}}, ensure_ascii=False))
    return 0


def stop_hook(event: dict) -> int:
    path = state_path(event.get("turn_id"))
    if not path.exists():
        print("{}")
        return 0
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("{}")
        return 0
    if state.get("status") == "ignored" or mtime_ns(DECISIONS) > int(state.get("decision_mtime_ns", 0)):
        path.unlink(missing_ok=True)
        print("{}")
        return 0
    if event.get("stop_hook_active"):
        print(json.dumps({"continue": False, "systemMessage": "결정 문서 후보가 아직 미해결이다. 반복 방지를 위해 종료하며 다음 턴에서 확인해야 한다."}, ensure_ascii=False))
        return 0
    excerpt = str(state.get("prompt_excerpt") or "").replace("\n", " ")[:240]
    reason = (
        "이 턴의 확정 의사결정 후보가 프로젝트 메모리에 반영되지 않았다. "
        f"후보 문장: {excerpt!r}. 확정 결정이면 docs/DECISIONS.md와 영향받는 기준 문서를 지금 갱신하라. "
        "확정 결정이 아니면 project_decision_memory.py resolve --turn-id <현재 turn_id> --ignore --reason <이유>로 해제하라."
    )
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


def resolve(turn_id: str, ignore: bool, reason: str) -> int:
    path = state_path(turn_id)
    if not path.exists():
        print(f"No pending decision candidate for turn {turn_id}", file=sys.stderr)
        return 1
    state = json.loads(path.read_text(encoding="utf-8"))
    if not ignore:
        return 2
    state["status"] = "ignored"
    state["resolution_reason"] = reason
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


def self_test() -> int:
    cases = {
        "zyte라는 걸로 크롤링을 하기로 했거든": True,
        "Zyte를 쓰기로 결정했습니다": True,
        "We decided to use Zyte for crawling.": True,
        "Zyte를 쓸지 결정해야 해": False,
        "Zyte 도입을 검토해보자": False,
        "어떤 도구가 좋을까?": False,
    }
    failures = [(text, expected, is_decision_candidate(text)) for text, expected in cases.items() if is_decision_candidate(text) != expected]
    if failures:
        print(json.dumps(failures, ensure_ascii=False), file=sys.stderr)
        return 1
    print(f"decision detector: {len(cases)} cases passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("prompt")
    sub.add_parser("stop")
    resolver = sub.add_parser("resolve")
    resolver.add_argument("--turn-id", required=True)
    resolver.add_argument("--ignore", action="store_true")
    resolver.add_argument("--reason", default="")
    sub.add_parser("self-test")
    args = parser.parse_args()
    if args.command == "prompt":
        return prompt_hook(read_event())
    if args.command == "stop":
        return stop_hook(read_event())
    if args.command == "resolve":
        return resolve(args.turn_id, args.ignore, args.reason)
    return self_test()


if __name__ == "__main__":
    raise SystemExit(main())
