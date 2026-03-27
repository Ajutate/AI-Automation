"""Configuration for AI Automation pipeline."""

import os
from dataclasses import dataclass


def _get_env(name: str, default: str) -> str:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


@dataclass(frozen=True)
class Config:
    litellm_base_url: str = _get_env("LITELLM_BASE_URL", "http://localhost:4000")
    litellm_api_key: str = _get_env("LITELLM_API_KEY", "anything")
    primary_model: str = _get_env("LITELLM_PRIMARY_MODEL", "qwen3")
    strong_model: str = _get_env("LITELLM_STRONG_MODEL", "qwen3")
    temperature: float = float(_get_env("LITELLM_TEMPERATURE", "0.0"))
    max_tokens: int = int(_get_env("LITELLM_MAX_TOKENS", "2048"))
    request_timeout_s: int = int(_get_env("LITELLM_TIMEOUT_S", "120"))

    output_feature_dir: str = _get_env("OUTPUT_FEATURE_DIR", "outputs/features")
    output_test_dir: str = _get_env("OUTPUT_TEST_DIR", "outputs/tests")
