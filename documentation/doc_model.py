from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class FileDocText:
    overview: str
    class_descriptions: Dict[str, str] = field(default_factory=dict)   # class_name -> text
    method_descriptions: Dict[str, str] = field(default_factory=dict)  # "Class.method" -> text
    function_descriptions: Dict[str, str] = field(default_factory=dict)  # function_name -> text
