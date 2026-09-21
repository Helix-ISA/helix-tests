import subprocess
import tempfile
from pathlib import Path

from .parser import load_state, load_tests


def run_test(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        import tomllib
        data = tomllib.load(f)

    tests = data["tests"]
    test_name = data.get("name", path.stem)
    description = data.get("description", "")

    print(f"[{test_name}]")
    if description:
        print(f"  {description}")
    print()

    passed = 0
    failed = 0

    for test in tests:
        print(f"  {test['name']}")

        with tempfile.TemporaryDirectory(prefix="helix-test-") as tmp:
            tmp = Path(tmp)

            asm_file = tmp / "program.hasm"
            binary_file = tmp / "program"
            state_file = tmp / "state.json"

            asm_file.write_text(
                "\n".join(test["program"]) + "\n"
            )

            subprocess.run(
                ["./hasm", str(asm_file), "-o", str(binary_file)],
                check=True,
            )

            subprocess.run(
                ["./hem", str(binary_file), "--dump-state", str(state_file)],
                check=True,
            )

            state = load_state(state_file)
            registers = test["expect"]["registers"]

            valid = True

            for register, expected in registers.items():
                index = int(register[1:])
                actual = state["registers"][index]

                if actual != expected:
                    print(
                        f"    FAIL: {register}: "
                        f"expected {expected}, got {actual}"
                    )
                    valid = False

            if valid:
                print("    PASS")
                passed += 1
            else:
                failed += 1

        print()

    if failed == 0:
        print(f"  File: PASS ({passed} passed, {failed} failed)")
    else:
        print(f"  File: FAIL ({passed} passed, {failed} failed)")

    print()

    return passed, failed
