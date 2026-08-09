import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from statistical_unit_gate import validate_donor_unit


class DonorUnitGateTests(unittest.TestCase):
    def test_multiple_cells_do_not_increase_donor_replicate_count(self):
        rows = [
            {"cell_id": "c1", "donor_id": "D1", "group": "control"},
            {"cell_id": "c2", "donor_id": "D1", "group": "control"},
            {"cell_id": "c3", "donor_id": "D2", "group": "RPL"},
            {"cell_id": "c4", "donor_id": "D2", "group": "RPL"},
        ]
        result = validate_donor_unit(rows)
        self.assertEqual(result["inferential_unit"], "donor")
        self.assertEqual(result["donors_by_group"], {"RPL": 1, "control": 1})
        self.assertFalse(result["cell_level_independence"])

    def test_cell_level_unit_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_donor_unit([], unit="cell")


if __name__ == "__main__":
    unittest.main()
