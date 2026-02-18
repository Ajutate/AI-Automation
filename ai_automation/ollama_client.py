"""Ollama client for text generation via local API."""

from typing import Optional
import requests
import logging

from .config import Config

logger = logging.getLogger(__name__)


def generate_text(prompt: str, model: Optional[str] = None, temperature: Optional[float] = None,
                  max_tokens: Optional[int] = None) -> str:
    cfg = Config()
    model_name = model or cfg.primary_model
    
    logger.info(f"🔄 Calling Ollama API - Model: {model_name}, Prompt length: {len(prompt)} chars")
    print(f"   📡 LLM Call: {model_name} (prompt: {len(prompt)} chars)")
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "temperature": temperature if temperature is not None else cfg.temperature,
        "stream": False,
        "options": {
            "num_predict": max_tokens if max_tokens is not None else cfg.max_tokens
        }
    }

    response = requests.post(
        f"{cfg.ollama_base_url}/api/generate",
        json=payload,
        timeout=cfg.request_timeout_s
    )
    response.raise_for_status()
    data = response.json()
    result = data.get("response", "").strip()
    
    print(f"   ✅ LLM Response: {len(result)} chars generated")
    logger.info(f"✅ Ollama response received - Generated: {len(result)} chars")
    
    return result
