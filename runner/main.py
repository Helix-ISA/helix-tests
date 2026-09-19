import sys
from pathlib import Path

from .runner import run_test

def main() -> int:
    tests_dir = Path("tests")

    tests = sorted(tests_dir.rglob("*.toml"))

    if not tests:
        print("No tests found.")
        return 1

    passed = 0
    failed = 0

    for test in tests:
        try:
            if run_test(test):
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

        print()
        print(f"Tests: {passed + failed}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
