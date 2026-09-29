import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/run_jev_coolblue_trial.py'
spec = importlib.util.spec_from_file_location('trial', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
EXISTING = Path(__file__).resolve().parents[1] / 'results_jev/20260928T060234KST/20260927T212511996048Z/coolblue'


class CoolblueTrialTests(unittest.TestCase):
    def test_five_blocks_selected_from_real_saved_evidence(self):
        jobs, source = m.select(EXISTING/'jev-request-drafts.jsonl', EXISTING/'jev-evidence.json')
        self.assertEqual([x['block_id'] for x in jobs], list(m.BLOCKS))
        self.assertEqual(source['page']['retailer'], 'coolblue')
        self.assertEqual(len(jobs), 5)
        self.assertTrue(all(len(x['payload']['questions']) == 3 for x in jobs))

    def test_offline_creates_five_requests_without_responses(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m, 'request_jev') as request:
                out = m.run(EXISTING/'jev-request-drafts.jsonl', EXISTING/'jev-evidence.json', False, Path(td))
            request.assert_not_called()
            self.assertEqual(len((out/'request-payloads.jsonl').read_text().splitlines()), 5)
            self.assertFalse((out/'responses.jsonl').exists())
            self.assertFalse(json.loads((out/'manifest.json').read_text())['api_called'])

    def test_live_cap_is_five_and_responses_are_block_linked(self):
        def fake(payload, key):
            self.assertEqual(key, 'fake')
            self.assertEqual(set(payload['questions']), {'ID19','ID20','ID23'})
            return {'model':'jev-1.13.0', 'answers':{
                item: {'type':'choice','choice':'does_not_match','confidence':0.8,
                       'probabilities':{'does_not_match':0.8,'matches':0.1,'evidence_missing':0.1}}
                for item in payload['questions']}, 'usage':{'input_tokens':100,'output_tokens':20}}
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m, 'api_key', return_value='fake'), patch.object(m, 'request_jev', side_effect=fake) as call:
                out = m.run(EXISTING/'jev-request-drafts.jsonl', EXISTING/'jev-evidence.json', True, Path(td))
            self.assertEqual(call.call_count, 5)
            responses = [json.loads(line) for line in (out/'responses.jsonl').read_text().splitlines()]
            self.assertEqual([row['block_id'] for row in responses], list(m.BLOCKS))
            self.assertTrue(json.loads((out/'manifest.json').read_text())['no_page_verdict'])
            self.assertNotIn('fake', (out/'manifest.json').read_text())

    def test_missing_key_fails_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m, 'api_key', return_value=None):
                with self.assertRaisesRegex(RuntimeError, 'TYPESAFE_API_KEY'):
                    m.run(EXISTING/'jev-request-drafts.jsonl', EXISTING/'jev-evidence.json', True, Path(td))
            self.assertEqual(list(Path(td).iterdir()), [])

    def test_partial_failure_preserves_successful_response(self):
        answer = {'model':'jev-1.13.0', 'answers':{
            mid: {'type':'choice', 'choice':'does_not_match', 'confidence':0.8,
                  'probabilities':{'does_not_match':0.8,'matches':0.1,'evidence_missing':0.1}}
            for mid in ('ID19','ID20','ID23')}}
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m, 'api_key', return_value='fake'), patch.object(
                    m, 'request_jev', side_effect=[answer, RuntimeError('temporary service failure')]):
                with self.assertRaisesRegex(RuntimeError, 'temporary service failure'):
                    m.run(EXISTING/'jev-request-drafts.jsonl', EXISTING/'jev-evidence.json', True, Path(td))
            output = next(Path(td).iterdir())
            self.assertEqual(len((output/'responses.jsonl').read_text().splitlines()), 1)
            manifest = json.loads((output/'manifest.json').read_text())
            self.assertEqual(manifest['status'], 'partial_error')
            self.assertEqual(manifest['request_count'], 1)


if __name__ == '__main__':
    unittest.main()
