"""Configuration for AI Automation pipeline."""

import os
from dataclasses import dataclass


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


@dataclass(frozen=True)
class Config:
    ollama_base_url: str = _get_env("OLLAMA_BASE_URL", "http://localhost:11434")
    primary_model: str = _get_env("OLLAMA_PRIMARY_MODEL", "qwen2.5:latest")
    strong_model: str = _get_env("OLLAMA_STRONG_MODEL", "qwen2.5:7b")
    temperature: float = float(_get_env("OLLAMA_TEMPERATURE", "0.2"))
    max_tokens: int = int(_get_env("OLLAMA_MAX_TOKENS", "2048"))
    request_timeout_s: int = int(_get_env("OLLAMA_TIMEOUT_S", "120"))

    output_feature_dir: str = _get_env("OUTPUT_FEATURE_DIR", "outputs/features")
    output_test_dir: str = _get_env("OUTPUT_TEST_DIR", "outputs/tests")
