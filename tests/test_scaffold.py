"""Structural checks: the package imports and the configs are consistent."""

import importlib
import pkgutil
from pathlib import Path

import pytest
import yaml

import geometry_of_safety

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "configs"
MODEL_CONFIGS = sorted((CONFIG_DIR / "models").glob("*.yaml"))
EXPERIMENT_CONFIGS = sorted((CONFIG_DIR / "experiments").glob("*.yaml"))
MODEL_NAMES = {path.stem for path in MODEL_CONFIGS}


def load(path: Path) -> dict:
    config = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(config, dict), f"{path.name} is not a mapping"
    return config


def test_all_modules_import():
    modules = pkgutil.walk_packages(geometry_of_safety.__path__, prefix="geometry_of_safety.")
    names = [module.name for module in modules]
    assert names, "no submodules found"
    for name in names:
        importlib.import_module(name)


def test_defaults_parse():
    load(CONFIG_DIR / "defaults.yaml")


def test_configs_exist():
    assert MODEL_CONFIGS and EXPERIMENT_CONFIGS


@pytest.mark.parametrize("path", MODEL_CONFIGS, ids=lambda path: path.stem)
def test_model_config(path):
    config = load(path)
    assert config["name"] == path.stem
    assert {"hf_id", "dtype", "n_layers", "d_model"} <= config.keys()


@pytest.mark.parametrize("path", EXPERIMENT_CONFIGS, ids=lambda path: path.stem)
def test_experiment_config(path):
    config = load(path)
    assert config["name"] == path.stem

    referenced = set(config.get("models", []))
    referenced |= {config[key] for key in ("source_model", "target_model") if key in config}
    assert referenced, "experiment names no model"
    assert referenced <= MODEL_NAMES, f"unknown models: {referenced - MODEL_NAMES}"

    assert (REPO_ROOT / "scripts" / f"{path.stem}.py").is_file(), "no matching script"
