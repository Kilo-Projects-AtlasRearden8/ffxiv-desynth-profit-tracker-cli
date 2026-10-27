# Project Status: FFXIV Desynth Profit Tracker CLI

## What Was Built

A Python CLI tool for FFXIV players to log desynth results, track profit per item, and export data to CSV. A fan project by Asdale Dynamics, LLC.

**Package structure:**
- `ffxiv_desynth_tracker/` - main package
  - `__init__.py` - version marker
  - `__main__.py` - enables `python -m ffxiv_desynth_tracker` execution
  - `storage.py` - Local JSON file storage: load/save, auto-incrementing IDs, auto-timestamps, corrupt file handling, directory creation
  - `profit.py` - Price math: `compute_profit()`, `entry_profit()`, `aggregate_by_item()`, `totals()`, margin calculation
  - `cli.py` - Argparse CLI with subcommands: `log`, `profit`, `list`, `export`, `--storage` flag
- `tests/`
  - `test_price_math.py` - 7 tests covering profit, aggregates, totals, margins, zero-earning edge case
  - `test_storage.py` - 5 tests covering load/save, ID increment, corrupt/missing files
- `pyproject.toml` - setuptools build config with console script entry point
- `README.md` - usage docs, install guide, CLI reference, credit to Asdale Dynamics, LLC
- `LICENSE` - MIT License with exact copyright: `Copyright (c) 2026 Asdale Dynamics, LLC`
- `.gitignore` - ignores `__pycache__/`, `*.pyc`, `*.egg-info/`, `dist/`, `build/`, `.venv/`, `venv/`, `env/`, `.desynth_entries.json`, `*.log`

**CLI Commands:**
```
ffxiv-desynth-tracker log <item> [--earned N] [--cost N] [--result success|fail] [--level N]
ffxiv-desynth-tracker profit [<item>]
ffxiv-desynth-tracker list
ffxiv-desynth-tracker export <path.csv>
ffxiv-desynth-tracker --storage <path> ...
```

**Data model (JSON entry):**
```json
{"id": 1, "timestamp": "...", "item": "...", "result": "success", "level": 500, "earned": 5000.0, "cost": 1000.0}
```

## How to Run

```bash
# Run tests
python3 -m unittest discover -s tests -v

# Run CLI directly (no install needed)
python3 -m ffxiv_desynth_tracker --help

# Install in a virtual environment for the ffxiv-desynth-tracker command
python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# Example workflow
python3 -m ffxiv_desynth_tracker log "Mythril Ingot" --earned 5000 --cost 1000 --result success
python3 -m ffxiv_desynth_tracker profit
python3 -m ffxiv_desynth_tracker export my_log.csv
```

## Verification Results

| Check | Status |
|-------|--------|
| All 12 unit tests pass | ✅ PASS |
| CLI help displays correctly (`python -m ffxiv_desynth_tracker --help`) | ✅ PASS |
| `log` command records entries with auto-id and timestamp | ✅ PASS |
| `profit` shows per-item and total aggregates with margins | ✅ PASS |
| `list` displays formatted table of all entries | ✅ PASS |
| `export` writes valid CSV with headers and computed profit column | ✅ PASS |
| Storage persists across runs (JSON file, `--storage` flag + env var) | ✅ PASS |
| Package builds and installs in venv (`pip install -e .`) | ✅ PASS |
| Console script `ffxiv-desynth-tracker` works after install | ✅ PASS |
| End-to-end workflow (log → profit → list → export) works | ✅ PASS |
| LICENSE contains exact required copyright line | ✅ PASS |
| README credits Asdale Dynamics, LLC | ✅ PASS |
| No secrets, API keys, or personal data in files | ✅ PASS |
| No `.github/workflows/` files | ✅ PASS |

## Known Gaps / Future Improvements

1. **No persistent install on system Python** - Requires venv/pipx due to PEP 668 (Debian/Ubuntu default). This is standard behavior, not a bug.
2. **No configuration file** - Storage path only via CLI flag or env var. Could add `~/.config/ffxiv-desynth-tracker/config.json`.
3. **No data migration** - Schema changes require manual JSON edit.
4. **Limited desynth result modeling** - Only `success`/`fail` result; no specific material/materia output tracking.
5. **No TUI or interactive mode** - Pure CLI only.
6. **No price lookup integration** - Manual `--earned`/`--cost` entry only. Could integrate with market board APIs (would require network).
7. **Single-file JSON storage** - Not concurrent-safe. Acceptable for personal CLI use.
8. **No delete/edit commands** - Entries are append-only. Could add `edit` and `delete` subcommands.
9. **No summary by desynth level** - Could add grouping by level for skill-up tracking.
10. **Test coverage** - Currently 12 tests. Could add integration tests for full CLI workflows using subprocess.