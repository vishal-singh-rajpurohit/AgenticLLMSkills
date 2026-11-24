"""Run all tests for agent-token-efficiency."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent


def load_all_tests() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_file in sorted(TESTS_ROOT.rglob("test_*.py")):
        spec = importlib.util.spec_from_file_location(f"tok_eff_{test_file.stem}", test_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Cannot load {test_file}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        suite.addTests(loader.loadTestsFromModule(mod))
    return suite


def main() -> int:
    verbosity = 2 if "-v" in sys.argv or "--verbose" in sys.argv else 1
    result = unittest.TextTestRunner(verbosity=verbosity).run(load_all_tests())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
