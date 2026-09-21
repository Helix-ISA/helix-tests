import json
import tomllib
from pathlib import Path


def load_tests(path: Path) -> list[dict]:
    with path.open("rb") as f:
        data = tomllib.load(f)

    return data["tests"]


def load_state(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
