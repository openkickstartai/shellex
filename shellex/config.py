"""Configuration management for shellex."""
import os
from pathlib import Path
from typing import Dict, Any

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_CONFIG = {
    "model": "llama3.2",
    "shell": "bash",
    "auto_execute": False,
    "history": True,
}


def config_path() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return Path(xdg) / "shellex" / "config.yml"


def load_config() -> Dict[str, Any]:
    """Load config from file, falling back to defaults."""
    path = config_path()
    if not path.exists():
        return DEFAULT_CONFIG.copy()
    if yaml is None:
        return DEFAULT_CONFIG.copy()
    try:
        with open(path) as f:
            user_config = yaml.safe_load(f) or {}
        merged = DEFAULT_CONFIG.copy()
        merged.update(user_config)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()
