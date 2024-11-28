# MIT License
#
# Copyright (c) 2024 - 2024 Wick Dynex
#
# Permission is hereby granted, free of charge,
# to any person obtaining a copy of this software and associated documentation files (the 'Software'),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software
# and to permit persons to whom the Software is furnished to do so
#
# The above copyright notice
# and this permission notice
# shall be included in all copies or substantial portions of the Software.
import os
import sys
from datetime import datetime
from io import StringIO
from unittest.mock import MagicMock, patch
import pytest

from src.license_arg_config import LicenseArgConfig


@pytest.fixture
def config():
    """Fixture to provide an instance of LicenseArgConfig for tests."""
    return LicenseArgConfig()


# Test valid argument parsing
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
def test_parse_valid_args(mock_parse_args, mock_exit, config):
    """Test that valid command-line arguments are parsed correctly."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./output",
    )

    config.parse()

    assert config.license_file == "license.json"
    assert config.license_type == "MIT License"
    assert config.start_year == 2020
    assert config.author == "John Doe"
    assert config.end_year == 2024
    assert config.target_folder == "./output"


# Test invalid start year > end year
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_invalid_start_year_greater_than_end_year(
    mock_access, mock_isdir, mock_parse_args, mock_exit, config
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
        config.parse()
        mock_print.assert_called_with(
            f"Error: Start year {current_year + 1} cannot be greater than end year {current_year}."
        )


# Test invalid end year in future
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_end_year_in_future(
    mock_access, mock_isdir, mock_parse_args, mock_exit, config
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
        config.parse()
        mock_print.assert_called_with(
            f"Error: End year 2025 cannot be in the future. Current year is {datetime.now().year}."
        )


# Test when the target folder does not exist
@patch("os.path.isdir", return_value=False)
@patch("os.access", return_value=True)
@patch("sys.exit")
def test_target_folder_not_exists(mock_exit, mock_access, mock_isdir, config):
    """Test that an error is raised when the target folder does not exist."""
    test_args = [
        "program_name",
        "--license-file", "path/to/license/file",
        "--license-type", "MIT",
        "--start-year", "2020",
        "--author", "John Doe",
        "--target-folder", "non_existent_folder",
    ]

    with patch.object(sys, "argv", test_args):
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            config.parse()
            output = mock_stdout.getvalue()
            assert "Error: Target folder 'non_existent_folder' does not exist." in output
            mock_exit.assert_called_once()


# Test missing --license-file argument
def test_missing_license_file(config):
    """Test that the --license-file argument is required."""
    with patch.object(
        sys,
        "argv",
        [
            "script_name",
            "--license-type", "MIT",
            "--start-year", "2020",
            "--author", "Author",
            "--target-folder", "/path/to/folder",
        ],
    ):
        with pytest.raises(SystemExit) as cm:
            config.parse()
        assert cm.value.code == 2


# Test missing --license-type argument
def test_missing_license_type(config):
    """Test that the --license-type argument is required."""
    with patch.object(
        sys,
        "argv",
        [
            "script_name",
            "--license-file", "license.txt",
            "--start-year", "2020",
            "--author", "Author",
            "--target-folder", "/path/to/folder",
        ],
    ):
        with pytest.raises(SystemExit) as cm:
            config.parse()
        assert cm.value.code == 2


# Test missing --start-year argument
def test_missing_start_year(config):
    """Test that the --start-year argument is required."""
    with patch.object(
        sys,
        "argv",
        [
            "script_name",
            "--license-file", "license.txt",
            "--license-type", "MIT",
            "--author", "Author",
            "--target-folder", "/path/to/folder",
        ],
    ):
        with pytest.raises(SystemExit) as cm:
            config.parse()
        assert cm.value.code == 2


# Test missing --author argument
def test_missing_author(config):
    """Test that the --author argument is required."""
    with patch.object(
        sys,
        "argv",
        [
            "script_name",
            "--license-file", "license.txt",
            "--license-type", "MIT",
            "--start-year", "2020",
            "--target-folder", "/path/to/folder",
        ],
    ):
        with pytest.raises(SystemExit) as cm:
            config.parse()
        assert cm.value.code == 2


# Test missing --target-folder argument
def test_missing_target_folder(config):
    """Test that the --target-folder argument is required."""
    with patch.object(
        sys,
        "argv",
        [
            "script_name",
            "--license-file", "license.txt",
            "--license-type", "MIT",
            "--start-year", "2020",
            "--author", "Author",
        ],
    ):
        with pytest.raises(SystemExit) as cm:
            config.parse()
        assert cm.value.code == 2


# Test valid folder check
@patch("sys.exit")
@patch("argparse.ArgumentParser.parse_args")
def test_valid_folder_check(mock_parse_args, mock_exit, config):
    """Test that the target folder exists validation works correctly."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./data",
    )

    config.parse()
    assert config.target_folder == "./data"


# Test the --detail flag is set to True
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_detail_flag(mock_isdir, mock_access, mock_parse_args, config):
    """Test that the --detail flag works correctly."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./output",
        detail=True,  # Simulate --detail being set to True
    )

    mock_isdir.return_value = True
    mock_access.return_value = True

    config.parse()

    assert config.detail is True


# Test the --detail flag is not set (default to False)
@patch("argparse.ArgumentParser.parse_args")
@patch("os.path.isdir")
@patch("os.access")
def test_no_detail_flag(mock_isdir, mock_access, mock_parse_args, config):
    """Test that the --detail flag is not set, so the 'detail' flag is False."""
    mock_parse_args.return_value = MagicMock(
        license_file="license.json",
        license_type="MIT License",
        start_year=2020,
        author="John Doe",
        end_year=2024,
        target_folder="./output",
        detail=False,  # Simulate --detail being absent (False)
    )

    mock_isdir.return_value = True
    mock_access.return_value = True

    config.parse()

    assert config.detail is False
