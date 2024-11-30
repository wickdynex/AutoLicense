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
Unit tests for the LicenseManager class in the 'src.license_manager' module.

This module contains test cases for the LicenseManager class, which is responsible
for managing license headers in source code files. The tests cover various methods
and functionalities, such as checking if a license file exists, adding a license to
files, and verifying if a license is present in a file's content.

Tested functionalities include:
- Checking and adding licenses to files that do or do not exist.
- Handling files with different extensions and formats (e.g., .cpp, .html).
- Verifying the presence of a license in a file's content.
- Formatting licenses with different comment styles (single-line, multi-line, XML/HTML).

Modules tested:
- `LicenseManager`
"""
from unittest.mock import mock_open, patch
import pytest
from src.license_manager import CommentStyle, FileType, LicenseManager


@pytest.fixture
def license_manager():
    """
    Fixture to create and return a LicenseManager instance with sample license text.
    This will be used in the test functions that require a LicenseManager object.
    """
    license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
    return LicenseManager(license_text, detail=True)


@patch("os.path.exists")
def test_check_and_add_license_file_not_exist(mock_exists, license_manager):
    """
    Test that ensures the license manager handles the case when a file does
    not exist. Specifically, this test simulates a scenario where a file
    doesn't exist and checks if an appropriate error message is printed.
    """
    # Simulate the file does not exist
    mock_exists.return_value = False

    # Test with a non-existent file path
    with patch("builtins.print") as mock_print:
        license_manager.check_and_add_license("test/testfile/non_existent.py")
        mock_print.assert_called_with(
            "[ERROR] The file test/testfile/non_existent.py does not exist."
        )


@patch("os.path.exists")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="MIT License\nCopyright 2015-2024 Microsoft Corporation",
)
def test_check_and_add_license_already_exists(mock_file, mock_exists, license_manager):
    """
    Test that ensures the license manager handles the case when a file
    already contains a license. It checks that the correct info message is printed
    when the license is successfully added to the file.
    """
    # Simulate that the file exists and already contains a license
    mock_exists.return_value = True

    # Simulate that the file already contains a license
    with patch("builtins.print") as mock_print:
        license_manager.check_and_add_license("test/testfile/existing_license.py")
        mock_print.assert_called_with(
            "[INFO] License added successfully to test/testfile/existing_license.py."
        )


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data="This is a test file.\n")
def test_check_and_add_license_html_comment(mock_file, mock_exists, license_manager):
    """
    Test that verifies the correct license is added to an HTML file using HTML-style comments.
    It checks if the license is correctly formatted and added at the beginning of the file.
    """
    # Simulate that the file exists, but does not contain a license
    mock_exists.return_value = True

    # Test an .html file, which should use HTML comments
    with patch("builtins.print") as mock_print:
        license_manager.check_and_add_license("test/testfile/test.html")

        # Check that the license was added successfully
        mock_print.assert_called_with(
            "[INFO] License added successfully to test/testfile/test.html."
        )

        # Check if the written license adheres to HTML comment format
        handle = mock_file()
        written_data = handle.write.call_args[0][0]
        assert written_data.startswith("<!--")  # HTML comments should start with '<!--'
        assert written_data.endswith("\n")  # HTML comments should end with '-->'


def test_is_license_present(license_manager):
    """
    Test that verifies the presence of a license in a file's content. It checks if
    the given content contains a valid license or not, based on the file type.
    """
    # Test when the file content contains the license
    content_with_license = (
        "/* MIT License\n"
        " * \n"
        " * Copyright (c) 2024 - 2024 Wick Dynex\n"
        " * \n"
        " */"
    )
    file_extension = ".cpp"  # Example file extension
    file_type = license_manager.get_file_type(file_extension)

    assert license_manager.is_license_present(content_with_license, file_type)

    # Test when the file content does not contain the license
    content_without_license = "Some random content here."
    assert not license_manager.is_license_present(content_without_license, file_type)


def test_get_file_type(license_manager):
    """
    Test the function that determines the file type based on the file extension.
    It checks the mapping of known file types (e.g., .cpp, .html) and also verifies
    that an unknown file type returns None.
    """
    # Test known file extensions
    assert license_manager.get_file_type(".cpp") == FileType.CPP
    assert license_manager.get_file_type(".html") == FileType.HTML

    # Test unknown file extension
    assert license_manager.get_file_type(".unknown") is None


def test_format_license_with_comments(license_manager):
    """
    Test the formatting of the license text into various comment styles (single-line,
    multi-line, XML/HTML comments). It verifies that the correct format is used based on
    the provided comment style.
    """
    # Test single-line comments
    formatted = license_manager.format_license_with_comments(
        CommentStyle.SINGLE_LINE.value
    )
    assert formatted.startswith("# MIT License")
    assert formatted.endswith("# Copyright 2015-2024 Microsoft Corporation")

    # Test multi-line comments
    formatted = license_manager.format_license_with_comments(
        CommentStyle.MULTI_LINE.value
    )
    assert formatted.startswith("/*")
    assert formatted.endswith(" */")

    # Test XML/HTML comments
    formatted = license_manager.format_license_with_comments(
        CommentStyle.XML_HTML.value
    )
    assert formatted.startswith("<!--")
    assert formatted.endswith("-->")
