from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

@dataclass(frozen=True)
class FileDiscoveryConfig:
    """
    Configuration for deterministic Python file discovery.
    """
    ignored_dir_names: frozenset[str] = frozenset(
        {
            ".git",
            "docs",
            "__pycache__",
            "venv",
            ".venv",
        }
    )
    ignore_hidden_dirs: bool = True


def discover_python_files(project_root: Path, config: FileDiscoveryConfig | None = None) -> List[Path]:
    """
    Recursively finds .py files under project_root.
    """
    if config is None:
        config = FileDiscoveryConfig()

    project_root = project_root.resolve()

    if not project_root.exists():
        raise FileNotFoundError(f"Project path does not exist: {project_root}")
    if not project_root.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {project_root}")

    results: List[Path] = []
    _walk_collect_py_files(project_root, project_root, config, results)

    results.sort(key=lambda p: p.as_posix())
    return results


def _walk_collect_py_files(
    current_dir: Path,
    project_root: Path,
    config: FileDiscoveryConfig,
    results_out: List[Path],
) -> None:
    """
    Deterministic DFS traversal. Directory entries are sorted lexicographically.
    """
    try:
        entries = sorted(current_dir.iterdir(), key=lambda p: p.name)
    except PermissionError:
        return

    for entry in entries:
        if entry.is_dir():
            if _should_skip_dir(entry, config):
                continue
            _walk_collect_py_files(entry, project_root, config, results_out)
        elif entry.is_file():
            if entry.suffix == ".py":
                results_out.append(entry.relative_to(project_root))


def _should_skip_dir(dir_path: Path, config: FileDiscoveryConfig) -> bool:
    name = dir_path.name

    if name in config.ignored_dir_names:
        return True

    if config.ignore_hidden_dirs and name.startswith("."):
        return True

    return False
