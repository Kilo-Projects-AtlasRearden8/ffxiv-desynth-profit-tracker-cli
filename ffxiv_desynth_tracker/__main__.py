"""Allow running the package with python -m ffxiv_desynth_tracker."""

from ffxiv_desynth_tracker.cli import main

if __name__ == "__main__":
    import sys

    sys.exit(main())
