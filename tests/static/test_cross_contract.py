"""Cross-tree contract guard (audit defect D2).

The whole-project audit found that ``contracts/`` and ``schemas/`` both carried
``ai/``, ``core/`` and ``identity/`` schemas, and that two of the duplicated
files had drifted apart (``core/contract-metadata.schema.json`` and
``identity/identity-boundary.schema.json``). The conflict was resolved in favour
of a single canonical source: ``schemas/``.

This test fails closed if a second schema tree (or any duplicated schema file)
reappears under ``contracts/``.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schemas"
CONTRACT_ROOT = ROOT / "contracts"

CANONICAL_SUBTREES = (
    "ai/ai-model.schema.json",
    "core/contract-metadata.schema.json",
    "identity/identity-boundary.schema.json",
)


class CrossContractTests(unittest.TestCase):

    def test_contracts_tree_carries_no_duplicate_schemas(self):
        if not CONTRACT_ROOT.exists():
            return

        duplicates = sorted(
            str(path.relative_to(ROOT))
            for path in CONTRACT_ROOT.glob("**/*.json")
        )

        self.assertEqual(
            duplicates,
            [],
            "contracts/ must not duplicate the canonical schemas/ tree: "
            f"{duplicates}",
        )

    def test_canonical_schema_subtrees_exist(self):
        for relative in CANONICAL_SUBTREES:
            self.assertTrue(
                (SCHEMA_ROOT / relative).is_file(),
                f"missing canonical schema: schemas/{relative}",
            )

    def test_schemas_tree_is_the_only_schema_source(self):
        self.assertTrue(
            any(SCHEMA_ROOT.rglob("*.schema.json")),
            "schemas/ must contain the canonical schema files",
        )


if __name__ == "__main__":
    unittest.main()
