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
