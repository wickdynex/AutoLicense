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
This script automatically adds license information to project files.

Usage:
    python main.py --license-file=LICENSE_FILE
                   --license-type=LICENSE_TYPE
                   --start-year=START_YEAR
                   --author=AUTHOR
                   --target-folder=TARGET_FOLDER
                   [--end-year=END_YEAR]
                   [--detail]

Arguments:
    --license-file=LICENSE_FILE     Path to the license file (e.g., LICENSE.txt).
    --license-type=LICENSE_TYPE     The type of the license (e.g., MIT, GPL-3.0).
    --start-year=START_YEAR         The start year for the license period (e.g., 2024).
    --author=AUTHOR                 The name or organization that holds the copyright.
    --target-folder=TARGET_FOLDER   The folder containing the project files to which the 
                                    license will be added.
    --end-year=END_YEAR             (Optional) The end year for the license period. Defaults 
                                    to the current year if not provided.
    --detail                        (Optional) If provided, outputs more detailed information 
                                    about the process.

This script will insert the specified license header into each file in the target folder, 
replacing any existing header with the updated license information.

Example usage:
    python main.py --license-file=LICENSE.txt --license-type=MIT --start-year=2024 
                   --author="John Doe" --target-folder="./src" --end-year=2025 --detail
"""
from src.auto_license import auto_license

if __name__ == "__main__":
    auto_license()
