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
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

from src.license_manager import CommentStyle, FileType, LicenseKeyword, LicenseManager


class TestLicenseManager(unittest.TestCase):
    @patch("os.path.exists")
    def test_check_and_add_license_file_not_exist(self, mock_exists):
        # Simulate the file does not exist
        mock_exists.return_value = False

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

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
    def test_check_and_add_license_already_exists(self, mock_file, mock_exists):
        # Simulate that the file exists and already contains a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Simulate that the file already contains a license
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/existing_license.py")
            mock_print.assert_called_with(
                "[INFO] License added successfully to test/testfile/existing_license.py."
            )

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file.\n")
    def test_check_and_add_license_html_comment(self, mock_file, mock_exists):
        # Simulate that the file exists, but does not contain a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

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
            self.assertTrue(
                written_data.startswith("<!--")
            )  # HTML comments should start with '<!--'
            self.assertTrue(
                written_data.endswith("\n")
            )  # HTML comments should end with '-->'

    def test_is_license_present(self):
        license_text = (
            "/* MIT License\n"
            " * \n"
            " * Copyright (c) 2024 - 2024 Wick Dynex\n"
            " * \n"
            " * Permission is hereby granted, free of charge,\n"
            " * to any person obtaining a copy of this software\n"
            " * and associated documentation files (the 'Software'),\n"
            " * to deal in the Software without restriction,\n"
            " * including without limitation the rights to use,\n"
            " * copy, modify, merge, publish, distribute,\n"
            " * sublicense, and/or sell copies of the Software\n"
            " * and to permit persons to whom the Software is\n"
            " * furnished to do so\n"
            " * \n"
            " * The above copyright notice\n"
            " * and this permission notice\n"
            " * shall be included in all copies or substantial\n"
            " * portions of the Software.\n"
            " */"
        )

        license_manager = LicenseManager(license_text, detail=True)

        file_extension = ".cpp"  # Example file extension
        file_type = license_manager.get_file_type(file_extension)

        # Test when the file content contains the license
        content_with_license = (
            "/* MIT License\n"
            " * \n"
            " * Copyright (c) 2024 - 2024 Wick Dynex\n"
            " * \n"
            " */"
        )
        self.assertTrue(
            license_manager.is_license_present(content_with_license, file_type)
        )

        # Test when the file content does not contain the license
        content_without_license = "Some random content here."
        self.assertFalse(
            license_manager.is_license_present(content_without_license, file_type)
        )

    def test_get_file_type(self):
        # Test the mapping of different file types
        license_manager = LicenseManager(
            "MIT License\nCopyright 2015-2024 Microsoft Corporation", detail=True
        )

        # Test known file extensions
        self.assertEqual(license_manager.get_file_type(".cpp"), FileType.CPP)
        self.assertEqual(license_manager.get_file_type(".html"), FileType.HTML)

        # Test unknown file extension
        self.assertIsNone(license_manager.get_file_type(".unknown"))

    def test_format_license_with_comments(self):
        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Test single-line comments
        formatted = license_manager.format_license_with_comments(
            CommentStyle.SINGLE_LINE.value
        )
        self.assertTrue(formatted.startswith("# MIT License"))
        self.assertTrue(
            formatted.endswith("# Copyright 2015-2024 Microsoft Corporation")
        )

        # Test multi-line comments
        formatted = license_manager.format_license_with_comments(
            CommentStyle.MULTI_LINE.value
        )
        self.assertTrue(formatted.startswith("/*"))
        self.assertTrue(formatted.endswith(" */"))

        # Test XML/HTML comments
        formatted = license_manager.format_license_with_comments(
            CommentStyle.XML_HTML.value
        )
        self.assertTrue(formatted.startswith("<!--"))
        self.assertTrue(formatted.endswith("-->"))


if __name__ == "__main__":
    unittest.main()
