# FFXIV Desynth Profit Tracker CLI

A small, local-first Python CLI for FFXIV players to log desynth results, track profit per item, and export CSV.

Built by Asdale Dynamics, LLC.

## Features

- Log desynth attempts with item name, gil earned, gil cost, and result
- Track profit per item with totals and margins
- Export all entries to CSV for spreadsheet analysis
- Local JSON storage — no network calls, no accounts
- Tested price math (profit, aggregates, margins)

## Install

```bash
pip install -e .
```

Or run directly without installing:

```bash
python -m ffxiv_desynth_tracker --help
```

## Usage

Log a desynth attempt:
```bash
ffxiv-desynth-tracker log "Mythril Ingot" --earned 5000 --cost 1000 --result success --level 500
```

Show profit for all items:
```bash
ffxiv-desynth-tracker profit
```

Show profit for a specific item:
```bash
ffxiv-desynth-tracker profit "Mythril Ingot"
```

List all logged entries:
```bash
ffxiv-desynth-tracker list
```

Export to CSV:
```bash
ffxiv-desynth-tracker export desynth_log.csv
```

Override storage location:
```bash
ffxiv-desynth-tracker --storage /path/to/my_log.json log "Item" --earned 100 --cost 50
```

Or set the `FFXIV_DESYNTH_STORAGE` environment variable.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.

## Disclaimer

This is a fan project. No game assets included. Not affiliated with Square Enix.