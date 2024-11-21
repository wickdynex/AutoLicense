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
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import MagicMock, patch

from src.license_arg_config import LicenseArgConfig


class TestLicenseArgConfig(unittest.TestCase):

    def setUp(self):
        """Set up mock values for testing"""
        self.config = LicenseArgConfig()

    # Mock sys.exit to prevent the program from exiting during tests
    @patch("sys.exit")
    @patch(
        "argparse.ArgumentParser.parse_args"
    )  # Mock parse_args to control input arguments
    def test_parse_valid_args(self, mock_parse_args, mock_exit):
        """Test that valid command-line arguments are parsed correctly"""
        # Simulate valid command-line arguments
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder="./output",
        )

        self.config.parse()

        # Check if all arguments are assigned correctly
        self.assertEqual(self.config.license_file, "license.json")
        self.assertEqual(self.config.license_type, "MIT License")
        self.assertEqual(self.config.start_year, 2020)
        self.assertEqual(self.config.author, "John Doe")
        self.assertEqual(self.config.end_year, 2024)
        self.assertEqual(self.config.target_folder, "./output")

    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    # Mock argparse's parse_args method
    @patch("argparse.ArgumentParser.parse_args")
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate folder existence
    @patch("os.access")  # Mock os.access to simulate folder write access
    def test_invalid_start_year_greater_than_end_year(
        self, mock_access, mock_isdir, mock_parse_args, mock_exit
    ):
        """Test that an error is raised when the start year is greater than the end year"""

        # Get the current year dynamically
        current_year = datetime.now().year

        # Simulate that the './output' folder exists
        mock_isdir.return_value = True

        # Simulate the behavior of os.access to return True (folder is
        # writable)
        mock_access.return_value = True

        # Simulate invalid command-line arguments (start year > end year)
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=current_year + 1,  # Start year is current year + 1
            author="John Doe",
            end_year=current_year,  # End year is current year (so start > end)
            target_folder="./output",
        )

        with patch("builtins.print") as mock_print:
            # Call the parse method, which should trigger the error for start
            # year > end year
            self.config.parse()

            # Check that the correct error message was printed
            mock_print.assert_called_with(
                f"Error: Start year {
                    current_year +
                    1} cannot be greater than end year {current_year}."
            )

    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    # Mock os.path.isdir to simulate directory existence check
    @patch("os.path.isdir")
    @patch("os.access")  # Mock os.access to simulate the write permission check
    # Mock argparse's parse_args method
    @patch("argparse.ArgumentParser.parse_args")
    def test_end_year_in_future(
        self, mock_parse_args, mock_access, mock_isdir, mock_exit
    ):
        """Test that an error is raised when the end year is in the future"""

        # Simulate invalid command-line arguments (end year is in the future)
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2025,  # End year in the future, should trigger the error
            detail=True,  # Ensure that 'detail' is set correctly in the mock
        )

        # Simulate the behavior of os.path.isdir to return True (folder exists)
        mock_isdir.return_value = True

        # Simulate the behavior of os.access to return True (folder is
        # writable)
        mock_access.return_value = True

        with patch("builtins.print") as mock_print:
            # Call the parse method to trigger argument validation
            self.config.parse()

            # Check if the correct error message was printed for end year in
            # the future
            mock_print.assert_called_with(
                "Error: End year 2025 cannot be in the future. Current year is 2024."
            )

    @patch(
        "os.path.isdir", return_value=False
    )  # Mock that the target folder does not exist
    # Mock that the folder is writable (not needed in this test, but just in
    # case)
    @patch("os.access", return_value=True)
    @patch("sys.exit")  # Mock sys.exit to prevent termination
    def test_target_folder_not_exists(self, mock_exit, mock_access, mock_isdir):
        # Create an instance of the LicenseArgConfig class
        config = LicenseArgConfig()

        # Test arguments to simulate command-line input
        test_args = [
            "program_name",  # Typically the script name is the first argument
            "--license-file",
            "path/to/license/file",
            "--license-type",
            "MIT",
            "--start-year",
            "2020",
            "--author",
            "John Doe",
            "--target-folder",
            "non_existent_folder",
        ]

        # Patch sys.argv to simulate command-line input
        with patch.object(sys, "argv", test_args):
            # Capture output using StringIO
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                # Call the parse method which will trigger validation
                config.parse()

                # Check that the error message was printed
                output = mock_stdout.getvalue()
                self.assertIn(
                    "Error: Target folder 'non_existent_folder' does not exist.", output
                )

                # Ensure sys.exit() was called due to the error
                mock_exit.assert_called_once()

    def test_missing_license_file(self):
        # Simulate missing --license-file argument
        with patch.object(
            sys,
            "argv",
            [
                "script_name",
                "--license-type",
                "MIT",
                "--start-year",
                "2020",
                "--author",
                "Author",
                "--target-folder",
                "/path/to/folder",
            ],
        ):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()

            # Check if SystemExit is called with the correct error code (2)
            self.assertEqual(cm.exception.code, 2)

    def test_missing_license_type(self):
        # Simulate missing --license-type argument
        with patch.object(
            sys,
            "argv",
            [
                "script_name",
                "--license-file",
                "license.txt",
                "--start-year",
                "2020",
                "--author",
                "Author",
                "--target-folder",
                "/path/to/folder",
            ],
        ):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()

            self.assertEqual(cm.exception.code, 2)

    def test_missing_start_year(self):
        # Simulate missing --start-year argument
        with patch.object(
            sys,
            "argv",
            [
                "script_name",
                "--license-file",
                "license.txt",
                "--license-type",
                "MIT",
                "--author",
                "Author",
                "--target-folder",
                "/path/to/folder",
            ],
        ):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()

            self.assertEqual(cm.exception.code, 2)

    def test_missing_author(self):
        # Simulate missing --author argument
        with patch.object(
            sys,
            "argv",
            [
                "script_name",
                "--license-file",
                "license.txt",
                "--license-type",
                "MIT",
                "--start-year",
                "2020",
                "--target-folder",
                "/path/to/folder",
            ],
        ):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()

            self.assertEqual(cm.exception.code, 2)

    def test_missing_target_folder(self):
        # Simulate missing --target-folder argument
        with patch.object(
            sys,
            "argv",
            [
                "script_name",
                "--license-file",
                "license.txt",
                "--license-type",
                "MIT",
                "--start-year",
                "2020",
                "--author",
                "Author",
            ],
        ):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()

            self.assertEqual(cm.exception.code, 2)

    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    @patch("argparse.ArgumentParser.parse_args")
    def test_valid_folder_check(self, mock_parse_args, mock_exit):
        """Test that the target folder exists validation works correctly"""
        # Simulate valid command-line arguments with a valid folder
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder="./data",
        )

        self.config.parse()
        self.assertEqual(self.config.target_folder, "./data")

    # Mock argparse's parse_args method
    @patch("argparse.ArgumentParser.parse_args")
    # Mock os.path.isdir to simulate directory existence check
    @patch("os.path.isdir")
    @patch("os.access")  # Mock os.access to simulate the write permission check
    def test_detail_flag(self, mock_isdir, mock_access, mock_parse_args):
        """Test that the --detail flag works correctly"""

        # Simulate command-line arguments with the --detail flag
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder="./output",
            detail=True,  # Simulate --detail being set to True
        )

        # Simulate the behavior of os.path.isdir to return False (folder
        # doesn't exist)
        mock_isdir.return_value = True

        # Simulate the behavior of os.access to return True (folder is
        # writable, should not be checked if folder doesn't exist)
        mock_access.return_value = True

        # Parse the arguments
        self.config.parse()

        # Check if the 'detail' flag is correctly set to True
        self.assertTrue(self.config.detail, "Expected 'detail' to be True")

    @patch(
        "argparse.ArgumentParser.parse_args"
    )  # Mock the parse_args method to simulate command-line input
    # Mock os.path.isdir to simulate directory existence check
    @patch("os.path.isdir")
    @patch("os.access")  # Mock os.access to simulate the write permission check
    def test_no_detail_flag(self, mock_isdir, mock_access, mock_parse_args):
        """Test that the --detail flag is not set, so the 'detail' flag is False"""

        # Simulate command-line arguments without the --detail flag
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder="./output",
            detail=False,  # Simulate --detail being absent (False)
        )

        # Simulate the behavior of os.path.isdir to return False (folder
        # doesn't exist)
        mock_isdir.return_value = True

        # Simulate the behavior of os.access to return True (folder is
        # writable, should not be checked if folder doesn't exist)
        mock_access.return_value = True

        # Parse the arguments
        self.config.parse()

        # Check if the 'detail' flag is correctly set to False
        self.assertFalse(self.config.detail, "Expected 'detail' to be False")


if __name__ == "__main__":
    unittest.main()
