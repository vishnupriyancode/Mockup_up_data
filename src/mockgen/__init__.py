"""Mock data generator package."""

from .core import (
    ensure_config_file,
    load_user_config,
    build_output_payload,
    build_indexed_records,
    write_output_file,
)

__all__ = [
    "ensure_config_file",
    "load_user_config",
    "build_output_payload",
    "build_indexed_records",
    "write_output_file",
]

__version__ = "0.1.0"


