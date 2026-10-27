"""Command line interface for the FFXIV desynth profit tracker."""

import argparse
import csv
import os
import sys

from .profit import aggregate_by_item, entry_profit, totals
from .storage import DEFAULT_STORAGE_PATH, Storage


def build_parser():
    parser = argparse.ArgumentParser(
        prog="ffxiv-desynth-tracker",
        description="Log FFXIV desynth results and track profit per item.",
    )
    parser.add_argument(
        "--storage",
        default=os.environ.get("FFXIV_DESYNTH_STORAGE", DEFAULT_STORAGE_PATH),
        help="Path to the JSON storage file.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Record a desynth attempt.")
    p_log.add_argument("item", help="Item name, e.g. 'Mythril Ingot'.")
    p_log.add_argument("--earned", type=float, default=0.0, help="Gil earned from the result.")
    p_log.add_argument("--cost", type=float, default=0.0, help="Gil spent on materials or desynth.")
    p_log.add_argument(
        "--result",
        choices=["success", "fail"],
        default="success",
        help="Desynth outcome.",
    )
    p_log.add_argument("--level", type=int, default=0, help="Desynth level used.")

    p_profit = sub.add_parser("profit", help="Show profit per item.")
    p_profit.add_argument("item", nargs="?", default=None, help="Optional item name to filter.")

    p_export = sub.add_parser("export", help="Export entries to CSV.")
    p_export.add_argument("path", help="Output CSV path.")

    sub.add_parser("list", help="List logged entries.")

    return parser


def cmd_log(args, storage):
    entry = {
        "item": args.item,
        "result": args.result,
        "earned": args.earned,
        "cost": args.cost,
        "level": args.level,
    }
    storage.add_entry(entry)
    print("Logged desynth of '{}': profit {:.0f} gil".format(args.item, entry_profit(entry)))
    return 0


def cmd_profit(args, storage):
    entries = storage.load()
    agg = aggregate_by_item(entries)
    if args.item:
        if args.item not in agg:
            print("No entries for '{}'.".format(args.item))
            return 0
        a = agg[args.item]
        print(
            "Profit for '{}': {:.0f} gil ({} attempts, earned {:.0f}, cost {:.0f}, margin {:.1f}%)".format(
                args.item, a["profit"], a["count"], a["earned"], a["cost"], a["margin"]
            )
        )
    else:
        if not agg:
            print("No entries yet.")
            return 0
        print("{:<28} {:>9} {:>10} {:>10} {:>10} {:>8}".format("Item", "Attempts", "Earned", "Cost", "Profit", "Margin"))
        for item, a in sorted(agg.items(), key=lambda kv: kv[1]["profit"], reverse=True):
            print("{:<28} {:>9} {:>10.0f} {:>10.0f} {:>10.0f} {:>7.1f}%".format(item, a["count"], a["earned"], a["cost"], a["profit"], a["margin"]))
        t = totals(entries)
        print("-" * 72)
        print("{:<28} {:>9} {:>10.0f} {:>10.0f} {:>10.0f}".format("TOTAL", "", t["earned"], t["cost"], t["profit"]))
    return 0


def cmd_export(args, storage):
    entries = storage.load()
    fieldnames = ["id", "timestamp", "item", "result", "level", "earned", "cost", "profit"]
    with open(args.path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            row = {fn: entry.get(fn, "") for fn in fieldnames}
            row["profit"] = entry_profit(entry)
            writer.writerow(row)
    print("Exported {} entries to {}".format(len(entries), args.path))
    return 0


def cmd_list(args, storage):
    entries = storage.load()
    if not entries:
        print("No entries yet.")
        return 0
    print("{:>4} {:<28} {:<8} {:>6} {:>9} {:>8} {:>9}".format("ID", "Item", "Result", "Level", "Earned", "Cost", "Profit"))
    for entry in entries:
        print("{:>4} {:<28} {:<8} {:>6} {:>9} {:>8} {:>9.0f}".format(
            entry.get("id", ""), str(entry.get("item", ""))[:28], str(entry.get("result", ""))[:8],
            entry.get("level", ""), entry.get("earned", ""), entry.get("cost", ""), entry_profit(entry)))
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = Storage(args.storage)
    if args.command == "log":
        return cmd_log(args, storage)
    if args.command == "profit":
        return cmd_profit(args, storage)
    if args.command == "export":
        return cmd_export(args, storage)
    if args.command == "list":
        return cmd_list(args, storage)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
