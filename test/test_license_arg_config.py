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
import unittest
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from io import StringIO
from datetime import datetime

from src.license_arg_config import LicenseArgConfig

class TestLicenseArgConfig(unittest.TestCase):
    
    def setUp(self):
        """Set up mock values for testing"""
        self.config = LicenseArgConfig()
        
    @patch("sys.exit")  # Mock sys.exit to prevent the program from exiting during tests
    @patch("argparse.ArgumentParser.parse_args")  # Mock parse_args to control input arguments
    def test_parse_valid_args(self, mock_parse_args, mock_exit):
        """Test that valid command-line arguments are parsed correctly"""
        # Simulate valid command-line arguments
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder='./output'
        )
        
        self.config.parse()

        # Check if all arguments are assigned correctly
        self.assertEqual(self.config.license_file, "license.json")
        self.assertEqual(self.config.license_type, "MIT License")
        self.assertEqual(self.config.start_year, 2020)
        self.assertEqual(self.config.author, "John Doe")
        self.assertEqual(self.config.end_year, 2024)
        self.assertEqual(self.config.target_folder, './output')
    
    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    @patch("argparse.ArgumentParser.parse_args")  # Mock the argparse's parse_args method
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate folder existence
    def test_invalid_start_year_greater_than_end_year(self, mock_isdir, mock_parse_args, mock_exit):
        """Test that an error is raised when the start year is greater than the end year"""
        
        # Get the current year dynamically
        current_year = datetime.now().year
        
        # Simulate that the './output' folder exists
        mock_isdir.return_value = True
        
        # Simulate invalid command-line arguments (start year > end year)
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=current_year + 1,  # Start year is current year + 1
            author="John Doe",
            end_year=current_year,  # End year is current year (so start > end)
            target_folder='./output'
        )
        
        with patch("builtins.print") as mock_print:
            # Call the parse method, which should trigger the error for start year > end year
            self.config.parse()
            
            # Check that the correct error message was printed
            mock_print.assert_called_with(f"Error: Start year {current_year + 1} cannot be greater than end year {current_year}.")

    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    @patch("argparse.ArgumentParser.parse_args")  # Mock the argparse's parse_args method
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate folder existence
    def test_end_year_in_future(self, mock_isdir, mock_parse_args, mock_exit):
        """Test that an error is raised when the end year is in the future"""
        
        # Get the current year dynamically
        current_year = datetime.now().year
        future_year = current_year + 1

        # Simulate that the './output' folder exists
        mock_isdir.return_value = True
        
        # Simulate invalid command-line arguments (end year in the future)
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=future_year,
            target_folder='./output'
        )
        
        with patch("builtins.print") as mock_print:
            # Call the parse method, which should trigger the error for end year in the future
            self.config.parse()
            
            # Check that the correct error message was printed
            mock_print.assert_called_with(f"Error: End year {future_year} cannot be in the future. Current year is {current_year}.")

    @patch("sys.exit")  # Mock sys.exit to prevent program termination
    @patch("argparse.ArgumentParser.parse_args")  # Mock argparse's parse_args method
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate directory existence check
    def test_target_folder_not_exists(self, mock_isdir, mock_parse_args, mock_exit):
        """Test that an error is raised when the target folder doesn't exist"""
        
        # Simulate invalid command-line arguments (non-existent target folder)
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024
        )
    
        # Set the target folder as a normal string, not MagicMock
        mock_parse_args.return_value.target_folder = './non_existent_folder'
        
        # Simulate the behavior of os.path.isdir to return False (folder doesn't exist)
        mock_isdir.return_value = False
        
        with patch("builtins.print") as mock_print:
            # Call the parse method to trigger argument validation
            self.config.parse()
            
            # Check if the correct error message was printed
            mock_print.assert_called_with("Error: Target folder './non_existent_folder' does not exist.")

    def test_missing_license_file(self):
        # Simulate missing --license-file argument
        with patch.object(sys, 'argv', ['script_name', '--license-type', 'MIT', '--start-year', '2020', '--author', 'Author', '--target-folder', '/path/to/folder']):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()
            
            # Check if SystemExit is called with the correct error code (2)
            self.assertEqual(cm.exception.code, 2)

    def test_missing_license_type(self):
        # Simulate missing --license-type argument
        with patch.object(sys, 'argv', ['script_name', '--license-file', 'license.txt', '--start-year', '2020', '--author', 'Author', '--target-folder', '/path/to/folder']):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()
            
            self.assertEqual(cm.exception.code, 2)

    def test_missing_start_year(self):
        # Simulate missing --start-year argument
        with patch.object(sys, 'argv', ['script_name', '--license-file', 'license.txt', '--license-type', 'MIT', '--author', 'Author', '--target-folder', '/path/to/folder']):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()
            
            self.assertEqual(cm.exception.code, 2)

    def test_missing_author(self):
        # Simulate missing --author argument
        with patch.object(sys, 'argv', ['script_name', '--license-file', 'license.txt', '--license-type', 'MIT', '--start-year', '2020', '--target-folder', '/path/to/folder']):
            with self.assertRaises(SystemExit) as cm:
                config = LicenseArgConfig()
                config.parse()
            
            self.assertEqual(cm.exception.code, 2)

    def test_missing_target_folder(self):
        # Simulate missing --target-folder argument
        with patch.object(sys, 'argv', ['script_name', '--license-file', 'license.txt', '--license-type', 'MIT', '--start-year', '2020', '--author', 'Author']):
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
            target_folder="./data"
        )
        
        self.config.parse()
        self.assertEqual(self.config.target_folder, "./data")

    @patch("argparse.ArgumentParser.parse_args")  # Mock the parse_args method to simulate command-line input
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate directory existence check
    def test_detail_flag(self, mock_isdir, mock_parse_args):
        """Test that the --detail flag works correctly"""
        
        # Simulate command-line arguments with the --detail flag
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder='./output',
            detail=True  # Simulate --detail being set to True
        )
        
        # Simulate the behavior of os.path.isdir to return False (folder doesn't exist)
        mock_isdir.return_value = True

        # Parse the arguments
        self.config.parse()
        
        # Check if the 'detail' flag is correctly set to True
        self.assertTrue(self.config.detail, "Expected 'detail' to be True")

    @patch("argparse.ArgumentParser.parse_args")  # Mock the parse_args method to simulate command-line input
    @patch("os.path.isdir")  # Mock os.path.isdir to simulate directory existence check
    def test_no_detail_flag(self, mock_isdir, mock_parse_args):
        """Test that the --detail flag is not set, so the 'detail' flag is False"""
        
        # Simulate command-line arguments without the --detail flag
        mock_parse_args.return_value = MagicMock(
            license_file="license.json",
            license_type="MIT License",
            start_year=2020,
            author="John Doe",
            end_year=2024,
            target_folder='./output',
            detail=False  # Simulate --detail being absent (False)
        )

        # Simulate the behavior of os.path.isdir to return False (folder doesn't exist)
        mock_isdir.return_value = True
        
        # Parse the arguments
        self.config.parse()
        
        # Check if the 'detail' flag is correctly set to False
        self.assertFalse(self.config.detail, "Expected 'detail' to be False")

if __name__ == "__main__":
    unittest.main()
