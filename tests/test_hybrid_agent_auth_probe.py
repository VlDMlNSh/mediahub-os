import json
import os
import unittest

import ops.qualification.hybrid_agent_auth_probe as probe


class HybridAgentAuthProbeTests(unittest.TestCase):
    def test_registered_cloud_provider_set_is_complete(self):
        ids = {p.id for p in probe.PROVIDERS}
        self.assertEqual(
            ids,
            {"gemini", "perplexity", "kimi", "deepseek", "chatgpt",
             "openrouter", "unorouter", "claude", "gigachat"},
        )

    def test_missing_credentials_fail_closed_without_secret_output(self):
        original = dict(os.environ)
        try:
            for p in probe.PROVIDERS:
                os.environ.pop(p.env, None)
            results = [probe.probe(p) for p in probe.PROVIDERS]
            self.assertTrue(all(r["status"] == "NOT_PROVEN" for r in results))
            encoded = json.dumps(results)
            self.assertNotIn("API_KEY", encoded)
        finally:
            os.environ.clear()
            os.environ.update(original)


if __name__ == "__main__":
    unittest.main()
