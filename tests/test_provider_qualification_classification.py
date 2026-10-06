import unittest

from ops.qualification.qualify_execution_backends import classify, classify_detail


class ProviderQualificationClassificationTests(unittest.TestCase):
    def test_http_402_is_insufficient_balance(self):
        self.assertEqual(classify(402, "payment required"), "insufficient_balance")
        self.assertEqual(classify_detail(402, "insufficient balance"), "insufficient_balance")

    def test_http_401_remains_authentication_error(self):
        self.assertEqual(classify(401, "unauthorized"), "authentication_or_authorization")

    def test_http_429_remains_rate_limit(self):
        self.assertEqual(classify(429, "quota exceeded"), "rate_limit_or_quota")


if __name__ == "__main__":
    unittest.main()
