import unittest

from runtime.mediahub_runtime.astra_security import redact, require_safe, scan_secret


class AstraSecurityTests(unittest.TestCase):
    def test_secret_like_values_are_detected_and_redacted(self):
        scan = scan_secret("authorization: Bearer abcdefghijklmnop")
        self.assertTrue(scan.detected)
        self.assertNotIn("abcdefghijklmnop", scan.redacted)
        self.assertIn("[REDACTED_SECRET]", scan.redacted)

    def test_common_non_secret_text_is_preserved(self):
        value = "project uses OpenAI-compatible API routing"
        self.assertFalse(scan_secret(value).detected)
        self.assertEqual(redact(value), value)

    def test_persistence_gate_rejects_secret_like_content(self):
        with self.assertRaisesRegex(ValueError, "content"):
            require_safe("api_key=abcdefghijklmnopqrstuvwxyz", "content")

    def test_optional_source_is_checked(self):
        with self.assertRaisesRegex(ValueError, "source"):
            require_safe("Bearer abcdefghijklmnop", "source")


if __name__ == "__main__":
    unittest.main()
