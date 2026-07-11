"""JSON save/load utilities with simple error handling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def save_json(data: Dict[str, Any], file_path: str | Path) -> Path:
    """Save a dictionary to a JSON file with indentation."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
    except OSError as exc:
        raise RuntimeError(f"Unable to save data to {path}: {exc}") from exc
    return path


def load_json(file_path: str | Path) -> Dict[str, Any]:
    """Load a dictionary from a JSON file."""
    path = Path(file_path)
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Saved data not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Saved JSON is invalid: {path}") from exc
    except OSError as exc:
        raise RuntimeError(f"Unable to read data file {path}: {exc}") from exc


def list_json_files(directory: str | Path) -> List[str]:
    """List JSON files in a directory."""
    path = Path(directory)
    if not path.exists():
        return []
    return sorted(str(item.name) for item in path.glob("*.json") if item.is_file())
