# FFXIV Desynth Profit Tracker CLI

A small, local-first Python CLI for FFXIV players to log desynth results, track profit per item, and export CSV.

**A fan project by Asdale Dynamics, LLC.** No game assets are included or distributed. Not affiliated with or endorsed by Square Enix.

---

## Why

Running desynths and selling the results is a great way to make gil in FFXIV — but it can be hard to tell which items are actually profitable. This tool keeps a simple local log of your desynth attempts, tracks how much you earn versus how much you spend, and lets you export the data so you can dig in further.

## Features

- **Log desynth attempts** — record item name, gil earned, gil spent, result (success/fail), and desynth level
- **Track profit per item** — see earnings, costs, net profit, and margin in one view
- **Export to CSV** — pull everything into a spreadsheet for deeper analysis
- **Local JSON storage** — your data stays on your computer. No accounts, no network calls, no uploads
- **Tested** — unit tests cover the profit math and storage behavior

---

## Quick Start

```bash
# Log a desynth attempt
ffxiv-desynth-tracker log "Mythril Ingot" --earned 5000 --cost 1000 --result success --level 500

# Check your profit across all items
ffxiv-desynth-tracker profit

# Export everything to CSV
ffxiv-desynth-tracker export my_desynth_log.csv
```

---

## Installation

### Option 1: Install (recommended for easy commands)

```bash
python3 -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -e .
```

### Option 2: Run directly (no install)

```bash
python3 -m ffxiv_desynth_tracker --help
```

---

## Commands

### `log` — Record a desynth attempt

```bash
ffxiv-desynth-tracker log <item> [options]

# Examples
ffxiv-desynth-tracker log "Mythril Ingot" --earned 5000 --cost 1000 --result success --level 500
ffxiv-desynth-tracker log "Iron Ore" --earned 100 --result fail
```

| Option       | Default   | Description                          |
|-------------|-----------|--------------------------------------|
| `--earned`  | `0`       | Gil earned from the desynth result   |
| `--cost`    | `0`       | Gil spent (materials, repairs)       |
| `--result`  | `success` | Outcome: `success` or `fail`         |
| `--level`   | `0`       | Desynth level used                   |

### `profit` — Show profit breakdown

```bash
# All items
ffxiv-desynth-tracker profit

# Single item
ffxiv-desynth-tracker profit "Mythril Ingot"
```

### `list` — Show all logged entries

```bash
ffxiv-desynth-tracker list
```

### `export` — Write entries to CSV

```bash
ffxiv-desynth-tracker export desynth_log.csv
```

The CSV includes: `id`, `timestamp`, `item`, `result`, `level`, `earned`, `cost`, and `profit`.

---

## Storage

By default, your data is stored in `desynth_entries.json` in your current directory. Override the location with:

- The `--storage` flag: `ffxiv-desynth-tracker --storage /path/to/log.json profit`
- The `FFXIV_DESYNTH_STORAGE` environment variable

---

## Data Format

Entries are stored as a JSON list inside `desynth_entries.json`:

```json
{
  "entries": [
    {
      "id": 1,
      "timestamp": "2026-10-27T15:02:00Z",
      "item": "Mythril Ingot",
      "result": "success",
      "level": 500,
      "earned": 5000.0,
      "cost": 1000.0
    }
  ]
}
```

---

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

All 12 tests cover price math (profit, aggregates, margins, edge cases) and storage behavior (load/save, ID increment, corrupt and missing files).

---

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.

This is a fan project, not affiliated with or endorsed by Square Enix.
