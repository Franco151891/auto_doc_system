from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
from update.hashing import sha256_file
from update.state_store import DocState


@dataclass(frozen=True)
class ChangeSet:
    changed: List[Path]   
    removed: List[Path]   


def detect_changes(project_root: Path, py_files: List[Path], prev_state: DocState) -> tuple[ChangeSet, Dict[str, str]]:
    
    new_hashes: Dict[str, str] = {}
    changed: List[Path] = []

    for rel_path in py_files:
        rel_key = rel_path.as_posix()
        abs_path = (project_root / rel_path).resolve()
        digest = sha256_file(abs_path)
        new_hashes[rel_key] = digest

        old_digest = prev_state.file_hashes.get(rel_key)
        if old_digest != digest:
            changed.append(rel_path)

    current_keys = set(new_hashes.keys())
    removed = [Path(k) for k in prev_state.file_hashes.keys() if k not in current_keys]

    return ChangeSet(changed=sorted(changed, key=lambda p: p.as_posix()),
                     removed=sorted(removed, key=lambda p: p.as_posix())), new_hashes
