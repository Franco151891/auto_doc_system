from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass(frozen=True)
class FunctionModel:
    name: str
    parameters: List[str] = field(default_factory=list)
    return_annotation: Optional[str] = None


@dataclass(frozen=True)
class MethodModel:
    name: str
    parameters: List[str] = field(default_factory=list)
    return_annotation: Optional[str] = None


@dataclass(frozen=True)
class ClassModel:
    name: str
    bases: List[str] = field(default_factory=list)
    methods: List[MethodModel] = field(default_factory=list)


@dataclass(frozen=True)
class FileModel:
    relative_path: Path
    imports: List[str] = field(default_factory=list)   # lo llenaremos en el siguiente paso
    classes: List[ClassModel] = field(default_factory=list)
    functions: List[FunctionModel] = field(default_factory=list)
