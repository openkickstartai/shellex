"""Tests for config module."""
from shellex.config import load_config, DEFAULT_CONFIG


def test_default_config():
    config = load_config()
    assert config["model"] == "llama3.2"
    assert config["shell"] == "bash"
    assert config["auto_execute"] is False
    assert config["history"] is True


def test_default_config_keys():
    config = load_config()
    for key in DEFAULT_CONFIG:
        assert key in config
