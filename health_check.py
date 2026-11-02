
"""Backward-compatible health-check entry point."""

from brain.health_check import check_brain


if __name__ == "__main__":
    success = check_brain()
    raise SystemExit(0 if success else 1)
