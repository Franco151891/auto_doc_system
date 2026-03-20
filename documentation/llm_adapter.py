from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


class LLMClient(Protocol):
    """
    Minimal interface for an LLM client.
    Must return plain text (no markdown), or raise an exception on failure.
    """
    def generate(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class LLMAdapterConfig:
    retry_once: bool = True
    placeholder_text: str = "<LLM_GENERATION_FAILED>"


class LLMAdapter:
    """
    Encapsulates LLM calls, retries once on failure, and returns placeholders if still failing.
    """
    def __init__(self, client: LLMClient, config: Optional[LLMAdapterConfig] = None) -> None:
        self._client = client
        self._config = config or LLMAdapterConfig()

    def generate_text(self, prompt: str) -> str:
        try:
            return self._client.generate(prompt).strip()
        except Exception:
            if not self._config.retry_once:
                return self._config.placeholder_text
        try:
            return self._client.generate(prompt).strip()
        except Exception:
            return self._config.placeholder_text
