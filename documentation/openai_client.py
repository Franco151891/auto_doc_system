from __future__ import annotations

import os
from openai import OpenAI


class OpenAIClient:
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def generate(self, prompt: str) -> str:
        resp = self._client.responses.create(
            model=self._model,
            input=prompt,
            max_output_tokens=120,  
        )
        
        return resp.output_text
