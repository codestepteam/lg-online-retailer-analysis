"""Offline workflow tests using disposable repositories, not the user's LG data."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

spec = importlib.util.spec_from_file_location("lg_research_memory", Path(__file__).with_name("lg_research_memory.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / module.REPO_NAMES[0]
        self.memory = module.Memory(self.root, self.base / "runtime")
        for name in module.REPO_NAMES:
            repo = self.base / name
            repo.mkdir()
            self.git(repo, "init", "-q")
            (repo / "sample.py").write_text("value = 1\n")
            (repo / ".gitignore").write_text(".env\n")
            if repo == self.root:
                for doc in module.DOCS:
                    path = repo / doc
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("# Original\n")
            self.git(repo, "add", ".")
            self.git(repo, "-c", "user.name=LG tests", "-c", "user.email=lg-tests@example.invalid", "commit", "-qm", "baseline")
        self.repo = self.base / "lg-pipeline"
        self.event = {"cwd": str(self.repo), "session_id": "session-one", "turn_id": "turn-one"}
        self.key = self.memory.key("session-one", "turn-one")
        self.findings = {"summary": "Test a newly observed LG rule", "findings": [
            {"kind": "observed", "text": "Only the saved input is used.", "source": "sample.py:1"},
        ]}

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def git(repo, *args):
        return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.DEVNULL)

    def start(self):
        return self.memory.prompt(self.event)

    def test_only_exact_three_roots_and_descendants(self):
        for name in module.REPO_NAMES:
            self.assertEqual(self.memory.scope(str(self.base / name / "nested")), self.base / name)
        for name in ("imagehub-root", "lg-pipeline-backup", "lg-crawling", "lg", ""):
            self.assertIsNone(self.memory.scope(str(self.base / name)))
        self.assertIsNone(self.memory.scope("relative/path"))

    def test_outside_event_has_no_state_or_context(self):
        event = {**self.event, "cwd": str(self.base / "imagehub-root")}
        self.assertEqual(self.memory.prompt(event), {})
        self.assertEqual(self.memory.stop(event), {})
        self.assertFalse(self.memory.state.exists())

    def test_no_prompt_or_transcript_contents_saved(self):
        event = {**self.event, "prompt": "SECRET-TEST-CONTENT", "transcript_path": "/private/chat"}
        self.memory.prompt(event)
        content = self.memory.path(self.key).read_text()
        self.assertNotIn("SECRET-TEST-CONTENT", content)
        self.assertNotIn("/private/chat", content)

    def test_missing_receipt_requests_one_continuation(self):
        self.start()
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")
        again = self.memory.stop({**self.event, "stop_hook_active": True})
        self.assertNotIn("decision", again)
        self.assertTrue(self.memory.load(self.key)["needs_attention"])

    def test_stop_without_prompt_can_be_completed(self):
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")
        self.assertTrue(self.memory.path(self.key).exists())

    def test_no_impact_receipt_and_later_source_change(self):
        self.start()
        self.memory.record(self.key, "no-impact", "Only a routine Git status lookup; no new LG knowledge.", [])
        self.assertEqual(self.memory.stop(self.event), {})
        (self.repo / "sample.py").write_text("value = 2\n")
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")

    def test_read_only_research_still_needs_a_receipt(self):
        self.start()
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")
        begin = self.memory.begin(self.key, self.findings)
        self.assertTrue(begin["acquired"])
        (self.root / "PROJECT_CONTEXT.md").write_text("# New observed rule\n")
        self.memory.record(self.key, "updated", "Recorded the read-only investigation and its source.", ["PROJECT_CONTEXT.md"])
        self.assertEqual(self.memory.stop(self.event), {})
        self.assertEqual(self.memory.pending(), [])

    def test_timestamp_only_change_cannot_claim_document_update(self):
        self.start()
        self.memory.begin(self.key, self.findings)
        (self.root / "PROJECT_CONTEXT.md").touch()
        with self.assertRaisesRegex(ValueError, "no document content changed"):
            self.memory.record(self.key, "updated", "A timestamp alone is not a content update.", ["PROJECT_CONTEXT.md"])
        self.memory.record(self.key, "already-documented", "Confirmed this exact finding already exists in the document.", ["PROJECT_CONTEXT.md"])
        self.assertEqual(self.memory.stop(self.event), {})

    def test_two_sessions_keep_distinct_notes_and_serialize_merge(self):
        self.start()
        first = self.memory.begin(self.key, self.findings)
        second_event = {**self.event, "session_id": "session-two"}
        second_key = self.memory.key("session-two", "turn-one")
        self.memory.prompt(second_event)
        second = self.memory.begin(second_key, self.findings)
        self.assertTrue(first["acquired"])
        self.assertFalse(second["acquired"])
        self.assertNotEqual(first["note"], second["note"])
        self.memory.record(second_key, "queued", "Another LG session owns the central document merge lock.", [])
        self.assertIn("systemMessage", self.memory.stop(second_event))
        self.assertEqual(len(self.memory.pending()), 2)
        self.memory.record(self.key, "already-documented", "Checked the finding against the existing central context.", ["PROJECT_CONTEXT.md"])
        self.assertTrue(self.memory.lock(second_key)["acquired"])
        (self.root / "PROJECT_CONTEXT.md").write_text("# Both sessions merged\n")
        self.memory.record(second_key, "updated", "Merged the queued note after the first session completed.", ["PROJECT_CONTEXT.md"])
        self.assertEqual(self.memory.pending(), [])

    def test_pending_finding_cannot_be_hidden_as_no_impact(self):
        self.start()
        self.memory.begin(self.key, self.findings)
        with self.assertRaisesRegex(ValueError, "cannot be hidden"):
            self.memory.record(self.key, "no-impact", "Pretending that the staged finding does not exist.", [])

    def test_expired_lock_cannot_authorize_a_stale_writer(self):
        self.start()
        self.memory.begin(self.key, self.findings)
        module.atomic_json(self.memory.state / "merge.json", {"owner": self.key, "until": time.time() - 1})
        (self.root / "PROJECT_CONTEXT.md").write_text("# Changes after lease expiration\n")
        with self.assertRaisesRegex(ValueError, "acquire the merge lock"):
            self.memory.record(self.key, "updated", "An expired lock must be acquired before finishing.", ["PROJECT_CONTEXT.md"])
        self.assertTrue(self.memory.lock(self.key)["acquired"])

    def test_note_tampering_requires_a_new_receipt(self):
        self.start()
        begin = self.memory.begin(self.key, self.findings)
        self.memory.record(self.key, "already-documented", "Checked this finding against the existing document content.", ["PROJECT_CONTEXT.md"])
        Path(begin["note"]).write_text("changed without recording\n")
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")

    def test_unrelated_central_update_does_not_invalidate_other_repo_receipt(self):
        self.start()
        self.memory.record(self.key, "no-impact", "No new LG knowledge from this routine inspection.", [])
        (self.root / "PROJECT_CONTEXT.md").write_text("# Updated by another session\n")
        self.assertEqual(self.memory.stop(self.event), {})

    def test_repeated_prompt_preserves_original_baseline(self):
        self.start()
        baseline = self.memory.load(self.key)
        (self.repo / "sample.py").write_text("value = 3\n")
        self.start()
        self.assertEqual(self.memory.load(self.key), baseline)

    def test_later_turn_can_integrate_an_older_pending_note(self):
        self.start()
        first = self.memory.begin(self.key, self.findings)
        self.memory.release(self.key)
        second_event = {**self.event, "turn_id": "later-turn"}
        later = self.memory.key("session-one", "later-turn")
        self.memory.prompt(second_event)
        relative = str(Path(first["note"]).relative_to(self.root))
        self.memory.begin(later, {**self.findings, "related_notes": [relative]})
        (self.root / "PROJECT_CONTEXT.md").write_text("# Integrated earlier research\n")
        self.memory.record(later, "updated", "Merged the old queued research and its sources into context.", ["PROJECT_CONTEXT.md"])
        self.assertEqual(self.memory.pending(), [])
        original = self.memory.load(self.key)
        self.assertEqual(original["integrated_by"], later)
        self.assertEqual(original["status"], "already-documented")

    def test_manual_setup_cannot_satisfy_a_real_hook_turn(self):
        manual = self.memory.maintenance(str(self.repo), "Install shared hooks before they have been activated.")
        self.memory.record(manual["turn"], "no-impact", "Only testing the setup record mechanism; no new facts.", [])
        self.start()
        self.assertEqual(self.memory.stop(self.event)["decision"], "block")
        self.assertNotEqual(manual["turn"], self.key)

    def test_paths_and_payload_are_validated(self):
        with self.assertRaises(ValueError):
            self.memory.path("../../escape")
        self.start()
        with self.assertRaises(ValueError):
            self.memory.begin(self.key, {"summary": "Missing evidence source", "findings": [{"kind": "observed", "text": "x"}]})
        with self.assertRaises(ValueError):
            self.memory.record(self.key, "no-impact", "A normal explanation without any new knowledge.", ["../outside.md"])


if __name__ == "__main__":
    unittest.main()
