"""Tests for price math."""

import unittest

from ffxiv_desynth_tracker.profit import aggregate_by_item, compute_profit, entry_profit, totals


class TestPriceMath(unittest.TestCase):
    def test_compute_profit_positive(self):
        self.assertEqual(compute_profit(5000, 1000), 4000)

    def test_compute_profit_negative(self):
        self.assertEqual(compute_profit(100, 500), -400)

    def test_compute_profit_zero(self):
        self.assertEqual(compute_profit(0, 0), 0)

    def test_entry_profit(self):
        self.assertEqual(entry_profit({"earned": 3000, "cost": 800}), 2200)

    def test_aggregate_by_item(self):
        entries = [
            {"item": "Mythril Ingot", "earned": 5000, "cost": 1000},
            {"item": "Mythril Ingot", "earned": 2000, "cost": 500},
            {"item": "Ore", "earned": 100, "cost": 0},
        ]
        agg = aggregate_by_item(entries)
        self.assertEqual(agg["Mythril Ingot"]["count"], 2)
        self.assertEqual(agg["Mythril Ingot"]["earned"], 7000)
        self.assertEqual(agg["Mythril Ingot"]["cost"], 1500)
        self.assertEqual(agg["Mythril Ingot"]["profit"], 5500)
        self.assertEqual(agg["Ore"]["profit"], 100)

    def test_totals(self):
        entries = [
            {"earned": 5000, "cost": 1000},
            {"earned": 2000, "cost": 500},
        ]
        t = totals(entries)
        self.assertEqual(t["earned"], 7000)
        self.assertEqual(t["cost"], 1500)
        self.assertEqual(t["profit"], 5500)

    def test_margin_zero_earned(self):
        agg = aggregate_by_item([{"item": "X", "earned": 0, "cost": 100}])
        self.assertEqual(agg["X"]["margin"], 0.0)


if __name__ == "__main__":
    unittest.main()
