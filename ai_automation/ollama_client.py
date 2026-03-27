"""LiteLLM client for text generation via OpenAI-compatible API."""

from typing import Optional
import requests
import logging

from .config import Config

logger = logging.getLogger(__name__)


def generate_text(prompt: str, model: Optional[str] = None, temperature: Optional[float] = None,
                  max_tokens: Optional[int] = None) -> str:
    cfg = Config()
    model_name = model or cfg.primary_model

    logger.info(f"🔄 Calling LiteLLM API - Model: {model_name}, Prompt length: {len(prompt)} chars")
    print(f"   📡 LLM Call: {model_name} (prompt: {len(prompt)} chars)")

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature if temperature is not None else cfg.temperature,
        "max_tokens": max_tokens if max_tokens is not None else cfg.max_tokens,
    }

    response = requests.post(
        f"{cfg.litellm_base_url}/v1/chat/completions",
        headers={"Authorization": f"Bearer {cfg.litellm_api_key}"},
        json=payload,
        timeout=cfg.request_timeout_s,
    )
    response.raise_for_status()
    result = response.json()["choices"][0]["message"]["content"].strip()

    print(f"   ✅ LLM Response: {len(result)} chars generated")
    logger.info(f"✅ LiteLLM response received - Generated: {len(result)} chars")

    return result
