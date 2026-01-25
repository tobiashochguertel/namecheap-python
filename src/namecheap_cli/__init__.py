"""Namecheap CLI - Command-line interface for Namecheap."""

import sys


def main() -> None:
    """Entry point with dependency checking."""
    try:
        from .__main__ import main as _main
    except ImportError as e:
        missing = str(e).split("'")[1] if "'" in str(e) else "unknown"
        print(
            f"❌ Error: Missing dependency '{missing}'.\n\n"
            "The CLI tool requires additional dependencies.\n"
            "Please install with:\n\n"
            "  uv tool install 'namecheap-python[cli]'\n\n"
            "Or for both CLI and TUI:\n\n"
            "  uv tool install 'namecheap-python[all]'\n",
            file=sys.stderr,
        )
        sys.exit(1)
    _main()


__all__ = ["main"]
