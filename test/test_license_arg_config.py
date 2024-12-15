# MIT License
#
# Copyright (c) 2024 - 2024 Wick Dynex
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software and associated documentation files
# (the 'Software'),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software
# and to permit persons to whom the Software is furnished to do so
#
# The above copyright notice
# and this permission notice
# shall be included in all copies or substantial portions of the Software.
"""
Unit tests for the LicenseArgConfig class.

This module contains a series of unit tests for the LicenseArgConfig class,
which is responsible for parsing and validating command-line arguments related
to licensing information. These tests cover various scenarios such as:
- Valid argument parsing
- Invalid start year greater than end year
- End year being in the future
- Various missing argument cases

The tests are implemented using pytest and unittest.mock for mocking external dependencies.
"""
from datetime import datetime
import pytest
from unittest.mock import MagicMock, patch
from src.license_arg_config import LicenseArgConfig


@pytest.fixture
def config_instance():
    """Fixture to provide an instance of LicenseArgConfig for tests."""
    return LicenseArgConfig()


# Test valid argument parsing
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
def test_parse_valid_args(mock_parse_args, mock_exit, config_instance):
    """Test that valid command-line arguments are parsed correctly."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./output",
    )

    config_instance.parse()

    assert config_instance.license_file == "license.json"
    assert config_instance.license_type == "MIT License"
    assert config_instance.start_year == 2020
    assert config_instance.author == "John Doe"
    assert config_instance.end_year == 2024
    assert config_instance.target_folder == "./output"

# Test case for --license-file argument
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
def test_parse_license_file(mock_parse_args, mock_exit, config_instance):
    """Test that the --license-file argument is parsed correctly."""

    # Mock the command-line arguments
    mock_parse_args.return_value = MagicMock(
        license_file="data/license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./output",
    )

    # Parse arguments
    config_instance.parse()

    # Assert that the license_file is correctly set
    assert config_instance.license_file == "data/license.json"
    assert config_instance.license_type == "MIT License"
    assert config_instance.start_year == 2020
    assert config_instance.author == "John Doe"
    assert config_instance.end_year == 2024
    assert config_instance.target_folder == "./output"

# Test case for --license-file argument with default value
def test_parse_license_file_default(monkeypatch, config_instance):
    """Test that the --license-file argument uses the default value when not provided."""

    # Simulate command-line arguments using monkeypatch
    # This simulates running the script with no --license-file argument
    monkeypatch.setattr('sys.argv', [
        'script_name',  # The script name (can be anything)
        '--license-type', 'MIT License',
        '--start-year', '2020',
        '--author', 'John Doe',
        '--end-year', '2024',
        '--target-folder', '.'
    ])

    # Parse arguments
    config_instance.parse()

    # Assert that the license_file uses the default value
    assert config_instance.license_file == "data/license.json"
    assert config_instance.license_type == "MIT License"
    assert config_instance.start_year == 2020
    assert config_instance.author == "John Doe"
    assert config_instance.end_year == 2024
    assert config_instance.target_folder == "."

# Test invalid start year > end year
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_invalid_start_year_greater_than_end_year(
    mock_access, mock_isdir, mock_parse_args, mock_exit, config_instance
):
    """Test that an error is raised when the start year is greater than the end year."""
    current_year = datetime.now().year

    mock_isdir.return_value = True
    mock_access.return_value = True

    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=current_year + 1,  # Start year is current year + 1
        author="John Doe",
        end_year=current_year,  # End year is current year (so start > end)
        target_folder="./output",
    )

    with patch("builtins.print") as mock_print:
        config_instance.parse()
        mock_print.assert_called_with(
            f"Error: Start year {current_year + 1} "
            f"cannot be greater than end year {current_year}."
        )


# Test invalid end year in future
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_end_year_in_future(
    mock_access, mock_isdir, mock_parse_args, mock_exit, config_instance
):
    """Test that an error is raised when the end year is in the future."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2025,  # End year in the future
        target_folder="./output",
    )

    mock_isdir.return_value = True
    mock_access.return_value = True

    with patch("builtins.print") as mock_print:
        config_instance.parse()
        mock_print.assert_called_with(
            f"Error: End year 2025 cannot be in the future. Current year is {datetime.now().year}."
        )


# Remove unused imports and parameters
