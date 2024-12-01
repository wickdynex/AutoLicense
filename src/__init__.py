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
Package for managing license headers in project files.

Modules:
    - LicenseArgConfig: Handles and validates license-related arguments.
    - LicenseGenerator: Generates license headers based on provided details.
    - LicenseManager: Applies license headers to project files.

Usage:
    Import the relevant classes to manage and apply license headers in your project.
"""
from .license_arg_config import LicenseArgConfig
from .license_generator import LicenseGenerator
from .license_manager import LicenseManager
