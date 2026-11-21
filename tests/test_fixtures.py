import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class FixtureTests(unittest.TestCase):
    def test_synthetic_records_match_documented_envelope(self):
        path = ROOT / 'fixtures' / 'records.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['dataset'], 'equity')
        self.assertIsInstance(data['records'], list)
        self.assertGreaterEqual(len(data['records']), 3)
        identifiers = [row['id'] for row in data['records']]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertTrue(all(isinstance(row, dict) for row in data['records']))

    def test_path_review_and_capacity_precede_booking_and_evidence(self):
        data = json.loads((ROOT / 'fixtures' / 'records.json').read_text(encoding='utf-8'))
        self.assertTrue({'objectives', 'paths', 'capacity'} <= set(data['catalogs']))
        reviews = [row for row in data['records'] if row['kind'] == 'equivalence-review']
        self.assertEqual({row['reviewer'] for row in reviews}, {'accessibility', 'writing-faculty'})
        self.assertTrue(any(row['kind'] == 'booking' for row in data['records']))
        self.assertTrue(any(row['kind'] == 'work-evidence' for row in data['records']))

if __name__ == '__main__':
    unittest.main()
