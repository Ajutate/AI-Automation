"""Output file utilities for generated feature and test files."""

from pathlib import Path
from typing import Tuple

from .config import Config


def save_outputs(feature_text: str, java_text: str, base_name: str) -> Tuple[str, str]:
    cfg = Config()
    feature_dir = Path(cfg.output_feature_dir)
    test_dir = Path(cfg.output_test_dir)

    feature_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    feature_path = feature_dir / f"{base_name}.feature"
    java_path = test_dir / f"{base_name}Test.java"

    feature_path.write_text(feature_text, encoding="utf-8")
    java_path.write_text(java_text, encoding="utf-8")

    return str(feature_path), str(java_path)
