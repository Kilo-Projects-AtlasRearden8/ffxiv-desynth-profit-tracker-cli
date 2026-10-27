# Project Status: FFXIV Desynth Profit Tracker CLI

## What Was Built

A Python CLI tool for FFXIV players to log desynth results, track profit per item, and export data to CSV.

**Package structure:**
- `ffxiv_desynth_tracker/` - main package
  - `storage.py` - Local JSON file storage with atomic writes, auto-creation of directories, corrupt file handling
  - `profit.py` - Price math: `compute_profit()`, `entry_profit()`, `aggregate_by_item()`, `totals()`
  - `cli.py` - Argparse-based CLI with subcommands: `log`, `profit`, `list`, `export`
  - `__init__.py` - version marker
- `tests/`
  - `test_price_math.py` - 7 tests covering profit calculations, aggregates, margins
  - `test_storage.py` - 5 tests covering load/save, id increment, corrupt/missing files
- `pyproject.toml` - setuptools build config with console script entry point
- `README.md` - usage instructions, install guide, credit to Asdale Dynamics, LLC
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

## How to Run

```bash
# Run tests
python3 -m unittest discover -s tests -v

# Run CLI directly (no install needed)
python3 -m ffxiv_desynth_tracker.cli --help

# Example workflow
python3 -m ffxiv_desynth_tracker.cli log "Mythril Ingot" --earned 5000 --cost 1000 --result success
python3 -m ffxiv_desynth_tracker.cli profit
python3 -m ffxiv_desynth_tracker.cli export my_log.csv
```

Install in a virtual environment for the `ffxiv-desynth-tracker` console command:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
ffxiv-desynth-tracker --help
```

## Verification Results

| Check | Status |
|-------|--------|
| All 12 unit tests pass | ✅ PASS |
| CLI help displays correctly | ✅ PASS |
| `log` command records entries with auto-id and timestamp | ✅ PASS |
| `profit` shows per-item and total aggregates with margins | ✅ PASS |
| `list` displays formatted table of all entries | ✅ PASS |
| `export` writes valid CSV with headers and computed profit column | ✅ PASS |
| Storage persists across runs (JSON file) | ✅ PASS |
| `--storage` flag and `FFXIV_DESYNTH_STORAGE` env var work | ✅ PASS |
| Package builds with setuptools (`pip install -e .` in venv) | ✅ PASS* |
| LICENSE contains exact required copyright line | ✅ PASS |
| README credits Asdale Dynamics, LLC | ✅ PASS |
| No secrets, API keys, or personal data in files | ✅ PASS |
| No `.github/workflows/` files | ✅ PASS |

* `pip install -e .` requires a virtual environment due to externally-managed Python environment (PEP 668). Verified working in venv.

## Known Gaps / Future Improvements

1. **No persistent install on system Python** - Requires venv/pipx due to PEP 668 (Debian/Ubuntu default). This is expected behavior for modern Python.
2. **No configuration file** - Storage path only via CLI flag or env var. Could add `~/.config/ffxiv-desynth-tracker/config.json`.
3. **No data migration** - Schema changes would require manual JSON edit.
4. **Limited desynth result modeling** - Only `success`/`fail` result, no specific material/materia output tracking.
5. **No TUI or interactive mode** - Pure CLI only.
6. **No price lookup integration** - Manual `--earned`/`--cost` entry only. Could integrate with Universalis/Market Board APIs (would require network).
7. **Single-file JSON storage** - Not concurrent-safe. For personal CLI use this is acceptable.
8. **No delete/edit commands** - Entries are append-only. Could add `edit` and `delete` subcommands.
9. **No summary by desynth level** - Could add grouping by level for skill-up tracking.
10. **Test coverage** - Currently 12 tests. Could add integration tests for full CLI workflows.

## Design Notes

- **Local-first**: All data stored in a local JSON file, no network calls.
- **Beginner-friendly**: Simple commands, clear output, no dependencies beyond stdlib (except setuptools for packaging).
- **Tested**: 12 unit tests covering price math edge cases and storage behavior.
- **FFXIV fan project disclaimer** in README.
- **No game assets** - purely a tracking tool.
- **MIT License** with required copyright attribution.