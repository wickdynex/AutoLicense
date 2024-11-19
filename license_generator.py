import json
from datetime import datetime
import sys
from typing import Optional

class LicenseGenerator:
    def __init__(self, license_file: str, license_type: str, start_year: int, end_year: Optional[int] = None, author: Optional[str] = None):
        """
        Initialize LicenseGenerator and load the license file contents.
        :param license_file: The path to the license.json file
        :param license_type: The type of the license to use (e.g., 'MIT License' or 'Apache License 2.0')
        :param start_year: The start year of the license
        :param end_year: The end year of the license (if not provided, defaults to the current year)
        :param author: The author of the license
        """
        if not license_type:
            print("Error: License type must be specified.")
            sys.exit(1)
        if not start_year:
            print("Error: Start year must be specified.")
            sys.exit(1)
        if author is None:
            print("Error: Author must be specified.")
            sys.exit(1)
        current_year = datetime.now().year
        if end_year is None:
            end_year = current_year
        if start_year > end_year:
            print(f"Error: Start year {start_year} cannot be greater than end year {end_year}.")
            sys.exit(1)
        if end_year > current_year:
            print(f"Error: End year {end_year} cannot be in the future. Current year is {current_year}.")
            sys.exit(1)
        self.license_file = license_file
        self.license_type = license_type
        self.start_year = start_year
        self.end_year = end_year
        self.author = author
        self.license_data = self._load_license_data()

    def _load_license_data(self):
        """Load the license data from the JSON file"""
        try:
            with open(self.license_file, 'r') as f:
                data = json.load(f)
                if self.license_type not in data["licenses"]:
                    print(f"Error: License type '{self.license_type}' not found in the license file.")
                    sys.exit(1)
                return data["licenses"][self.license_type]
        except FileNotFoundError:
            print(f"Error: License file '{self.license_file}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Failed to parse the license file '{self.license_file}'. Please check the file format.")
            sys.exit(1)

    def generate_license(self) -> str:
        """
        Generate the license text
        :return: The generated license string
        """
        copyright_text = " ".join(self.license_data["copyright"]).format(
            start_year=self.start_year, end_year=self.end_year, author=self.author
        )
        permissions_text = "\n".join(self.license_data["permissions"])
        conditions_text = "\n".join(self.license_data["conditions"])
        license_text = f"{self.license_type}\n\n{copyright_text}\n\n{permissions_text}\n\n{conditions_text}"
        return license_text

if __name__ == "__main__":
    try:
        license_generator_mit = LicenseGenerator(
            license_file="license.json", license_type="MIT License", start_year=2015, end_year=2024, author="Microsoft Corporation"
        )
        license_text_mit = license_generator_mit.generate_license()
        print("MIT License:\n")
        print(license_text_mit)
    except Exception as e:
        print(str(e))
    try:
        license_generator_apache = LicenseGenerator(
            license_file="license.json", license_type="Apache License 2.0", start_year=2015, end_year=None, author="Microsoft Corporation"
        )
        license_text_apache = license_generator_apache.generate_license()
        print("\nApache License 2.0:\n")
        print(license_text_apache)
    except Exception as e:
        print(str(e))
    try:
        license_generator_apache = LicenseGenerator(
            license_file="license.json", license_type="Apache License 2.0", start_year=None, end_year=None, author="Microsoft Corporation"
        )
        license_text_apache = license_generator_apache.generate_license()
        print("\nApache License 2.0:\n")
        print(license_text_apache)
    except Exception as e:
        print(str(e))
