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
import argparse
import os
import sys
from datetime import datetime


class LicenseArgConfig:
    def __init__(self):
        """
        Initialize LicenseArgConfig class for parsing command-line arguments.
        """
        self.license_file = None
        self.license_type = None
        self.start_year = None
        self.end_year = None
        self.author = None
        self.target_folder = None
        self.detail = False

    def parse(self):
        """
        Use argparse to parse command-line arguments, and validate their correctness.
        :return: Validated arguments
        """
        parser = argparse.ArgumentParser(
            description="Apply copyright information to all files in the specified target folder."
        )

        # Required arguments
        parser.add_argument(
            "--license-file", required=True, help="Path to the license file"
        )
        parser.add_argument(
            "--license-type",
            required=True,
            help="Type of the license (e.g., MIT License)",
        )
        parser.add_argument(
            "--start-year", type=int, required=True, help="Start year of the license"
        )

        # Optional argument
        parser.add_argument(
            "--end-year", type=int, help="End year of the license (optional)"
        )

        # Required arguments
        parser.add_argument("--author", required=True, help="Author of the license")

        # Target folder argument
        parser.add_argument(
            "--target-folder",
            required=True,
            help="Target folder containing files to which copyright will be applied",
        )

        # Optional argument
        parser.add_argument(
            "--detail",
            action="store_true",
            help="Show details on whether the license has been added to the files",
        )

        # Parse command-line arguments
        args = parser.parse_args()

        # Set the detail flag
        self.detail = args.detail

        # Validate parameters
        self._validate_args(args)

        # Assign parsed arguments to instance variables
        self.license_file = args.license_file
        self.license_type = args.license_type
        self.start_year = args.start_year
        self.author = args.author
        self.end_year = args.end_year
        # self.target_folder = os.path.abspath(args.target_folder)  # Ensure we
        # use an absolute path
        self.target_folder = args.target_folder

    def _validate_args(self, args):
        """
        Validate the parsed arguments to ensure their correctness.
        :param args: Parsed arguments
        """
        # Get the current year dynamically
        current_year = datetime.now().year

        # Check if start year is less than or equal to end year
        if args.end_year is not None and args.start_year > args.end_year:
            self._handle_error(
                f"Start year {
                    args.start_year} cannot be greater than end year {
                    args.end_year}."
            )

        # Check if end year is in the future
        if args.end_year is not None and args.end_year > current_year:
            self._handle_error(
                f"End year {
                    args.end_year} cannot be in the future. Current year is {current_year}."
            )

        # Check if target folder exists
        if not os.path.isdir(args.target_folder):
            self._handle_error(
                f"Target folder '{
                    args.target_folder}' does not exist."
            )

        # Check if the target folder is writable
        if not os.access(args.target_folder, os.W_OK):
            self._handle_error(
                f"Target folder '{
                    args.target_folder}' is not writable. Please ensure you have write permissions."
            )

    def _handle_error(self, message: str):
        """
        Prints the error message and exits the program.
        :param message: The error message to display
        """
        print(f"Error: {message}")
        sys.exit(1)

    def display_info(self):
        """Display the parsed command-line arguments in the specified order."""
        print(f"License file: {self.license_file}")
        print(f"License type: {self.license_type}")
        print(f"Start year: {self.start_year}")
        print(f"End year: {self.end_year if self.end_year else 'N/A'}")
        print(f"Author: {self.author}")
        print(f"Target folder: {self.target_folder}")
        print(f"Show details: {self.detail}")


def main():
    # Create LicenseArgConfig instance
    config = LicenseArgConfig()

    # Parse command-line arguments
    config.parse()

    # Display parsed arguments
    config.display_info()


if __name__ == "__main__":
    main()
