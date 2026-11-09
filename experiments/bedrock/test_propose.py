"""Offline checks only; no AWS clients or credentials."""

import copy
import json
import unittest
from unittest.mock import patch

import propose as p


class ProposalValidationTests(unittest.TestCase):
    def setUp(self):
        self.code = p.source()
        # Synthetic validator fixture, never presented as a model response.
        self.proposal = {"schema_version": 1, "target_path": p.TARGET,
            "source_sha256": p.sha(self.code), "diagnosis": "Synthetic test fixture.",
            "change": {"old": p.OLD, "new": "case 'Berlin':\n      return 'berlin';"}}

    def validate(self, proposal):
        return p.validate_proposal(json.dumps(proposal), self.code)

    def test_accepts_bounded_proposal_without_writing_source(self):
        self.assertEqual(self.validate(self.proposal), self.proposal)
        self.assertEqual(p.source(), self.code)

    def test_structure_does_not_prove_business_correctness(self):
        self.proposal["change"]["new"] = "case 'Berlin':\n      return 'munich';"
        self.validate(self.proposal)  # Allowed syntax; still wrong under independent tests.

    def test_rejects_other_paths_stale_hashes_and_extra_fields(self):
        variants = [dict(self.proposal, target_path="app/test/routing.test.mjs"),
                    dict(self.proposal, source_sha256="0" * 64),
                    dict(self.proposal, command="npm test"),
                    dict(self.proposal, schema_version=True)]
        for variant in variants:
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                self.validate(variant)

    def test_rejects_edits_outside_berlin_and_noop(self):
        for new in [p.OLD, "case 'Hamburg':\n      return 'berlin';",
                    "case 'Berlin':\n      return 'berlin';\nprocess.exit(0);", "", None]:
            proposal = copy.deepcopy(self.proposal)
            proposal["change"]["new"] = new
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.validate(proposal)

    def test_rejects_ambiguous_replacement(self):
        self.proposal["change"]["old"] = "return 'hamburg';"
        with self.assertRaises(ValueError):
            self.validate(self.proposal)

    def test_rejects_duplicate_keys_markdown_and_oversize(self):
        for text in ['{"schema_version":1,"schema_version":1}',
                     '```json\n' + json.dumps(self.proposal) + '\n```', 'x' * 8193, '[]']:
            with self.subTest(text=text[:40]), self.assertRaises(ValueError):
                p.validate_proposal(text, self.code)

    def test_rejects_truncation_and_tool_requests(self):
        response = {"stopReason": "end_turn", "output": {"message": {
            "role": "assistant", "content": [{"text": json.dumps(self.proposal)}]}}}
        p.validate_response(response, self.code)
        for reason in ["max_tokens", "tool_use", "guardrail_intervened"]:
            with self.subTest(reason=reason), self.assertRaises(ValueError):
                p.validate_response(dict(response, stopReason=reason), self.code)
        response["output"]["message"]["content"] = [{"toolUse": {}}]
        with self.assertRaises(ValueError):
            p.validate_response(response, self.code)

    def test_request_has_no_tools_and_fixed_model_region_limits(self):
        request = p.build_request()
        self.assertNotIn("toolConfig", request)
        self.assertEqual(request["modelId"], "amazon.nova-lite-v1:0")
        self.assertEqual(request["inferenceConfig"]["maxTokens"], 512)
        self.assertLess(len(json.dumps(request, ensure_ascii=False).encode()), p.MAX_INPUT_BYTES)

    def test_zero_quota_fails_closed(self):
        access = {"authorization": "AUTHORIZED", "region_availability": "AVAILABLE",
                  "entitlement": "AVAILABLE", "agreement": "AVAILABLE", "quotas": {"rpm": 0}}
        with self.assertRaisesRegex(ValueError, "Zero inference quota"):
            p.assert_access(access)

    def test_no_approval_never_opens_sdk(self):
        with patch("sys.argv", ["propose.py", "invoke"]), patch.object(p, "sdk_session") as session:
            with self.assertRaises(SystemExit) as error:
                p.main()
            self.assertEqual(error.exception.code, 2)
            session.assert_not_called()


if __name__ == "__main__":
    unittest.main()
