import json
from datetime import datetime
import sys

class LicenseGenerator:
    def __init__(self, license_file, license_type, start_year, author, end_year=None):
        """
        Initialize LicenseGenerator and load the license file contents.

        :param license_file: The path to the license.json file
        :param license_type: The type of the license to use (e.g., 'MIT License' or 'Apache License 2.0')
        :param start_year: The start year of the license
        :param author: The author of the license
        :param end_year: The end year of the license (if not provided, defaults to the current year)
        """
        # Check if license_type, start_year, and author are provided
        if not license_type:
            print("Error: License type must be specified.")
            sys.exit(1)

        if not start_year:
            print("Error: Start year must be specified.")
            sys.exit(1)

        if not author:
            print("Error: Author must be specified.")
            sys.exit(1)

        self.license_file = license_file
        self.license_type = license_type
        self.start_year = start_year
        self.author = author
        self.end_year = end_year if end_year else datetime.now().year  # If no end_year is provided, use the current year by default
        self.license_data = self._load_license_data()

    def _load_license_data(self):
        """Load the license data from the JSON file"""
        with open(self.license_file, 'r') as f:
            data = json.load(f)
            # Check if the specified license type exists in the file
            if self.license_type not in data["licenses"]:
                print(f"Error: License type '{self.license_type}' not found in the license file.")
                sys.exit(1)
            return data["licenses"][self.license_type]

    def generate_license(self):
        """
        Generate the license text

        :return: The generated license string
        """
        # Format the copyright text
        copyright_text = " ".join(self.license_data["copyright"]).format(
            start_year=self.start_year, end_year=self.end_year, author=self.author
        )

        # Format the permissions text
        permissions_text = "\n".join(self.license_data["permissions"])

        # Format the conditions text
        conditions_text = "\n".join(self.license_data["conditions"])

        # Combine all the parts into the final license text
        license_text = f"{self.license_type}\n\n{copyright_text}\n\n{permissions_text}\n\n{conditions_text}"
        return license_text


if __name__ == "__main__":
    # Create a LicenseGenerator object, specifying the license type (MIT License) and passing the start year and author

    # Example 1: Using MIT License
    try:
        license_generator_mit = LicenseGenerator(
            license_file="license.json", license_type="MIT License", start_year=2015, author="Microsoft Corporation", end_year=2024
        )
        license_text_mit = license_generator_mit.generate_license()
        print("MIT License:\n")
        print(license_text_mit)
    except Exception as e:
        print(str(e))

    # Example 2: Using Apache License 2.0
    try:
        license_generator_apache = LicenseGenerator(
            license_file="license.json", license_type="Apache License 2.0", start_year=2015, author="Microsoft Corporation"
        )
        license_text_apache = license_generator_apache.generate_license()
        print("\nApache License 2.0:\n")
        print(license_text_apache)
    except Exception as e:
        print(str(e))
    

    # Example 3: Using Apache License 2.0 (without start year, should trigger error)
    try:
        license_generator_apache = LicenseGenerator(
            license_file="license.json", license_type="Apache License 2.0", start_year=None, author="Microsoft Corporation"
        )
        license_text_apache = license_generator_apache.generate_license()
        print("\nApache License 2.0:\n")
        print(license_text_apache)
    except Exception as e:
        print(str(e))
