"""Persistence helpers for the gradebook JSON data file."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "gradebook.json"
LOG_PATH = ROOT_DIR / "logs" / "app.log"

logger = logging.getLogger("gradebook")
logger.setLevel(logging.INFO)
if not logger.handlers:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(LOG_PATH)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def default_data() -> dict[str, list[Any]]:
    """Return the empty-gradebook structure."""
    return {"students": [], "courses": [], "enrollments": []}


def load_data(path: str | Path | None = None) -> dict[str, list[Any]]:
    """Load gradebook JSON data from disk.

    If the file does not exist, an empty structure is returned.
    If the file contains invalid JSON, a helpful message is shown and an empty structure is used.
    """
    target = Path(path) if path else DATA_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            logger.info("No gradebook data file found at %s; starting empty.", target)
            return default_data()

        with target.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Gradebook data must be a JSON object.")

        logger.info("Loaded gradebook data from %s.", target)
        return data
    except FileNotFoundError:
        logger.warning("Data file missing: %s. Starting with an empty gradebook.", target)
        return default_data()
    except json.JSONDecodeError as exc:
        message = (
            f"The gradebook file at {target} is corrupted or not valid JSON. "
            f"Please fix it or delete it to start fresh. Error: {exc.msg}"
        )
        logger.error(message)
        print(f"Warning: {message}")
        return default_data()
    except (TypeError, ValueError, OSError) as exc:
        logger.error("Unexpected error while reading gradebook data: %s", exc)
        print(f"Warning: Unable to read gradebook data: {exc}")
        return default_data()


def save_data(data: dict[str, list[Any]], path: str | Path | None = None) -> None:
    """Persist gradebook JSON data to disk."""
    target = Path(path) if path else DATA_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
            file.write("\n")
        logger.info("Saved gradebook data to %s.", target)
    except FileNotFoundError:
        logger.error("Could not save to %s because the directory does not exist.", target)
        raise
    except OSError as exc:
        logger.exception("Error saving gradebook data: %s", exc)
        raise
