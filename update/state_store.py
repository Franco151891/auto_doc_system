from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

STATE_DIR_NAME = ".auto_doc"
STATE_FILE_NAME = "state.json"


@dataclass(frozen=True)
class DocState:
    file_hashes: Dict[str, str]  


def load_state(project_root: Path) -> DocState:
    state_path = _state_file_path(project_root)
    if not state_path.exists():
        return DocState(file_hashes={})

    data = json.loads(state_path.read_text(encoding="utf-8"))
    hashes = data.get("file_hashes", {})
    if not isinstance(hashes, dict):
        hashes = {}
    clean: Dict[str, str] = {}
    for k, v in hashes.items():
        if isinstance(k, str) and isinstance(v, str):
            clean[k] = v
    return DocState(file_hashes=clean)


def save_state(project_root: Path, state: DocState) -> None:
    state_dir = _state_dir_path(project_root)
    state_dir.mkdir(parents=True, exist_ok=True)

    payload = {"file_hashes": state.file_hashes}
    _state_file_path(project_root).write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _state_dir_path(project_root: Path) -> Path:
    return project_root / STATE_DIR_NAME


def _state_file_path(project_root: Path) -> Path:
    return _state_dir_path(project_root) / STATE_FILE_NAME
