"""Tests for JSON storage."""

import os
import tempfile
import unittest

from ffxiv_desynth_tracker.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.storage = Storage(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_empty_storage_returns_empty_list(self):
        self.assertEqual(self.storage.load(), [])

    def test_add_and_load_entry(self):
        entry = self.storage.add_entry({"item": "Mythril Ingot", "earned": 5000, "cost": 1000})
        self.assertEqual(entry["id"], 1)
        self.assertIn("timestamp", entry)
        entries = self.storage.load()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["item"], "Mythril Ingot")

    def test_ids_increment(self):
        self.storage.add_entry({"item": "A"})
        self.storage.add_entry({"item": "B"})
        entries = self.storage.load()
        self.assertEqual(entries[0]["id"], 1)
        self.assertEqual(entries[1]["id"], 2)

    def test_missing_file_returns_empty_list(self):
        storage = Storage("/nonexistent/path/entries.json")
        self.assertEqual(storage.load(), [])

    def test_corrupt_file_returns_empty_list(self):
        with open(self.path, "w") as fh:
            fh.write("not json")
        self.assertEqual(self.storage.load(), [])


if __name__ == "__main__":
    unittest.main()
