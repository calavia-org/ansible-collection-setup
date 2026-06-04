# tests/integration/test_integration.py

"""Tests for molecule scenarios."""

from __future__ import absolute_import, division, print_function

import platform

import pytest
from pytest_ansible.molecule import MoleculeScenario


# Scenarios that should only run on specific platforms
PLATFORM_SPECIFIC_SCENARIOS = {
    "darwin": "Darwin",
}


def test_integration(molecule_scenario: MoleculeScenario) -> None:
    """Run molecule for each scenario.

    :param molecule_scenario: The molecule scenario object
    """
    scenario_name = molecule_scenario.name
    current_platform = platform.system()

    # Skip platform-specific scenarios on unsupported platforms
    if scenario_name in PLATFORM_SPECIFIC_SCENARIOS:
        required_platform = PLATFORM_SPECIFIC_SCENARIOS[scenario_name]
        if current_platform != required_platform:
            pytest.skip(
                f"Scenario '{scenario_name}' requires platform '{required_platform}', "
                f"but current platform is '{current_platform}'"
            )

    proc = molecule_scenario.test()
    assert proc.returncode == 0
