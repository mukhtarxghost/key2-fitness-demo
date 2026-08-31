"""
LLM Provider — Abstraction layer for language model backends.

Swap implementations without rewriting application code.
Active:  Groq via groq SDK.
Fallback: Gemini via google-genai SDK.
"""

import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

load_dotenv()


class LLMProvider(ABC):
    """Base interface every LLM provider must implement."""

    @abstractmethod
    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Send a system + user prompt to the LLM,
        return the text response.
        """
        ...


# ---------------------------------------------------------------------------
# Groq
# ---------------------------------------------------------------------------

class GroqProvider(LLMProvider):
    """Groq implementation — fast inference via Groq Cloud."""

    def __init__(self):
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Add it to your .env file."
            )
        self._client = Groq(api_key=api_key)
        self._model = os.getenv(
            "GROQ_MODEL", "llama-3.1-8b-instant"
        )

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Gemini (fallback)
# ---------------------------------------------------------------------------

class GeminiProvider(LLMProvider):
    """Google Gemini implementation."""

    def __init__(self):
        from google import genai
        from google.genai import types

        self._types = types
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file."
            )
        self._client = genai.Client(api_key=api_key)
        self._model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self._client.models.generate_content(
            model=self._model,
            contents=user_prompt,
            config=self._types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        return response.text


# ---------------------------------------------------------------------------
# Provider factory
# ---------------------------------------------------------------------------

_provider_instance = None


def get_llm_provider() -> LLMProvider:
    """
    Return the active LLM provider.

    Set LLM_PROVIDER env var to switch:
      - "groq"    (default)
      - "gemini"
    """
    global _provider_instance

    if _provider_instance is not None:
        return _provider_instance

    provider_name = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider_name == "groq":
        _provider_instance = GroqProvider()
    elif provider_name == "gemini":
        _provider_instance = GeminiProvider()
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {provider_name}")

    return _provider_instance
