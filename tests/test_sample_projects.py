"""
Integration tests for the FawltyDeps project

Check for given a simple project that following workflows work:
- discover all imports and dependencies
  and correctly identify unused and missing dependencies
- TODO given only part of the project to search in
  correctly identify unused and missing dependencies

Sample projects are subdirectories of `tests/sample_projects`. These are
auto-discovered and used in `sample_projects_params` below.

The structure of sample project is as follows:

tests/sample_projects
├── sample_project1
│   ├── expected.toml (mandatory)
│   └── ... (regular Python project)
└── sample_project2
    ├── expected.toml (mandatory)
    └── ... (regular Python project)
"""
import sys
from pathlib import Path

import pytest

from fawltydeps.main import Action, Analysis

if sys.version_info >= (3, 11):
    import tomllib  # pylint: disable=E1101
else:
    import tomli as tomllib

# These are (slow) integration tests that are disabled by default.
pytestmark = pytest.mark.integration

SAMPLE_PROJECTS_DIR = Path(__file__).with_name("sample_projects")

sample_projects_params = [
    pytest.param(sample_project, id=sample_project.name)
    for sample_project in SAMPLE_PROJECTS_DIR.iterdir()
    if sample_project.is_dir()
]


@pytest.mark.parametrize("project_path", sample_projects_params)
def test_integration_analysis_on_sample_projects__(project_path):

    actions = {Action.REPORT_UNDECLARED, Action.REPORT_UNUSED}
    analysis = Analysis.create(actions, code=project_path, deps=project_path)

    with (project_path / "expected.toml").open("rb") as f:
        expected = tomllib.load(f)

    assert (
        analysis.unused_deps
        == set(expected.get("analysis_result", {}).get("unused_deps"))
        or set()
    )
    assert set(analysis.undeclared_deps.keys()) == set(
        expected.get("analysis_result", {}).get("undeclared_deps") or {}
    )
