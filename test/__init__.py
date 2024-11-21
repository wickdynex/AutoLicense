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
# __init__.py

# This file marks the 'test' directory as a Python package.
# It is used for package-level control, allowing easier import of submodules.

# Import specific functions or classes from submodules to make them accessible from the package level.
# This enables users to import directly from 'test' instead of specifying
# submodule names.

# Import test modules
from .test_license_arg_config import *
from .test_license_generator import *

# Optionally, you could also import specific classes, functions, or variables from these modules
# Example:
# from .test_license_arg_config import LicenseArgConfig
# from .test_license_generator import LicenseGenerator

# If you want to add initialization logic for the package, you can add it here.
# For example, you can initialize logging, configuration, etc.
# print("Initializing the 'test' package...")
