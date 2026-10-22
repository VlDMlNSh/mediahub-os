import json
import tempfile
import unittest
from pathlib import Path

from tools import validate_contracts


class Draft202012ValidationTests(unittest.TestCase):
    def write_schema(self, data):
        temporary = tempfile.TemporaryDirectory(prefix="mediahub-schema-")
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "schema.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_canonical_schema_passes_meta_schema_validation(self):
        path = validate_contracts.SCHEMA_ROOT / "core/contract-metadata.schema.json"
        self.assertTrue(validate_contracts.validate_schema(path))

    def test_invalid_json_schema_keyword_fails_closed(self):
        path = self.write_schema({
            "$schema": validate_contracts.DRAFT_2020_12,
            "$id": "https://example.invalid/test-schema",
            "type": "not-a-json-schema-type",
        })
        with self.assertRaises(SystemExit):
            validate_contracts.validate_schema(path)

    def test_unknown_format_name_fails_closed(self):
        path = self.write_schema({
            "$schema": validate_contracts.DRAFT_2020_12,
            "$id": "https://example.invalid/test-schema",
            "type": "string",
            "format": "date-tmie",
        })
        with self.assertRaises(SystemExit):
            validate_contracts.validate_schema(path)

    def test_format_like_data_in_examples_is_not_treated_as_schema(self):
        path = self.write_schema({
            "$schema": validate_contracts.DRAFT_2020_12,
            "$id": "https://example.invalid/test-schema",
            "type": "object",
            "examples": [{"format": "application-specific-value"}],
        })
        self.assertFalse(validate_contracts.validate_schema(path))

    def _metadata_schema(self, schema_version):
        return {
            "$schema": validate_contracts.DRAFT_2020_12,
            "$id": "https://example.invalid/metadata-schema",
            "type": "object",
            "properties": {
                "schema_id": {"type": "string"},
                "schema_version": schema_version,
                "owner": {"type": "string"},
            },
        }

    def test_boolean_schema_version_metadata_fails_closed(self):
        # Boolean subschemas are valid Draft 2020-12, but are not a valid
        # declaration of the required string-valued metadata version.
        path = self.write_schema(self._metadata_schema(False))
        with self.assertRaises(SystemExit):
            validate_contracts.validate_schema(path)

    def test_non_string_schema_version_const_fails_closed(self):
        # The JSON Schema meta-schema allows a number-valued const under a
        # string type; the metadata envelope must reject this contradiction.
        path = self.write_schema(self._metadata_schema({
            "type": "string",
            "const": 42,
        }))
        with self.assertRaises(SystemExit):
            validate_contracts.validate_schema(path)

    def test_format_checker_accepts_valid_date_time(self):
        schema = {"type": "string", "format": "date-time"}
        validator = validate_contracts.build_validator(schema)
        self.assertTrue(validator.is_valid("2026-10-19T20:00:00Z"))

    def test_format_checker_rejects_invalid_date_time(self):
        schema = {"type": "string", "format": "date-time"}
        validator = validate_contracts.build_validator(schema)
        self.assertFalse(validator.is_valid("yesterday at eight"))

    def test_format_checker_rejects_invalid_uri(self):
        schema = {"type": "string", "format": "uri"}
        validator = validate_contracts.build_validator(schema)
        self.assertFalse(validator.is_valid("not a uri"))


if __name__ == "__main__":
    unittest.main()
