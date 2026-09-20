import subprocess
import tempfile
from pathlib import Path

from .parser import load_state, load_test

def run_test(path: Path) -> bool:
    test = load_test(path)

    print(f"Running: {test['name']}")

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
            check=True
        )

        subprocess.run(
            ["./hem", str(binary_file), "--dump-state", str(state_file)],
            check=True
        )

        registers = test["expect"]["registers"]
        valid = True

        state = load_state(state_file)

        for register, expected in registers.items():
            index = int(register[1:])

            actual = state["registers"][index]

            if actual != expected:
                print(
                        f"FAIL: {register}: "
                        f"expected {expected}, got {actual}"
                )
                valid = False
            else:
                print("PASS")

    return True
