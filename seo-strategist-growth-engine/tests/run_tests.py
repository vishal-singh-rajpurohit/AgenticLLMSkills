"""Discover and execute all test_*.py suites across seo-strategist-growth-engine/tests."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parent


def load_all_tests() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for idx, test_file in enumerate(sorted(TESTS_ROOT.rglob("test_*.py"))):
        module_name = f"growth_engine_test_{idx}_{test_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, test_file)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load test module: {test_file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def main() -> int:
    verbosity = 2 if "-v" in sys.argv or "--verbose" in sys.argv else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(load_all_tests())
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
