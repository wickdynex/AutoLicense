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
import argparse
from src.license_arg_config import LicenseArgConfig
from src.license_generator import LicenseGenerator
from src.license_manager import LicenseManager

def auto_license():
    config = LicenseArgConfig()
    config.parse()
    config.display_info()

    generator = LicenseGenerator(config.license_file, 
                                 config.license_type,
                                 config.start_year, 
                                 config.end_year, 
                                 config.author)
    license_text = generator.generate_license()

    license_manager = LicenseManager(license_text, config.detail)

    for root, dirs, files in os.walk(config.target_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            license_manager.check_and_add_license(file_path)


if __name__ == '__main__':
    auto_license()
