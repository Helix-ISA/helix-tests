import tomllib
import json
from pathlib import Path

def load_test(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)

def load_state(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
