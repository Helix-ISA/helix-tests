import tomllib
from pathlib import Path

def load_test(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)
