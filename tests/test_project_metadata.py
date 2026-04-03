"""Regression tests for witch.audio packaging and startup defaults."""

from pathlib import Path
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_project():
    pyproject_path = REPO_ROOT / "pyproject.toml"
    with pyproject_path.open("rb") as handle:
        return tomllib.load(handle)["project"]


def test_pyproject_parses_and_uses_witch_package_name():
    project = _load_project()

    assert project["name"] == "witch-audio-agent"
    assert project["scripts"]["witch"] == "hermes_cli.main:main"


def test_all_extra_includes_matrix_dependency():
    optional_dependencies = _load_project()["optional-dependencies"]

    assert "matrix" in optional_dependencies
    assert "witch-audio-agent[matrix]" in optional_dependencies["all"]


def test_config_example_preloads_witch_identity_skill():
    config_text = (REPO_ROOT / "cli-config.yaml.example").read_text(encoding="utf-8")

    assert "skills:" in config_text
    assert "startup:" in config_text
    assert "witch-audio-identity" in config_text
