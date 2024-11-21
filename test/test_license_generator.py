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
import json
import unittest
from unittest.mock import mock_open, patch

from src.license_generator import LicenseGenerator


class TestLicenseGenerator(unittest.TestCase):

    def setUp(self):
        # Mocked license data
        self.license_data = {
            "licenses": {
                "MIT License": {
                    "copyright": ["Copyright {start_year}-{end_year} {author}."],
                    "permissions": [
                        "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:"
                    ],
                    "conditions": [
                        "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."
                    ],
                },
                "Apache License 2.0": {
                    "copyright": ["Copyright {start_year}-{end_year} {author}."],
                    "permissions": [
                        "You may use the Software in compliance with the License."
                    ],
                    "conditions": [
                        "You must include a copy of the License in any distribution of the Software."
                    ],
                },
            }
        }

    def test_generate_license_mit(self):
        """Test generating the MIT license"""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.license_data))):
            # Create LicenseGenerator instance for MIT License
            license_generator = LicenseGenerator(
                license_file="license.json",
                license_type="MIT License",
                start_year=2015,
                end_year=2024,
                author="Microsoft Corporation",
            )
            generated_license = license_generator.generate_license()

            # Expected license text for MIT License
            expected_license = (
                "MIT License\n\nCopyright 2015-2024 Microsoft Corporation.\n\n"
                + "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\n"
                + "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."
            )
            # Assert that the generated license matches the expected license
            self.assertEqual(generated_license, expected_license)

    def test_generate_license_apache(self):
        """Test generating the Apache License 2.0"""
        with patch("builtins.open", mock_open(read_data=json.dumps(self.license_data))):
            # Create LicenseGenerator instance for Apache License 2.0
            license_generator = LicenseGenerator(
                license_file="license.json",
                license_type="Apache License 2.0",
                start_year=2015,
                end_year=2024,
                author="Microsoft Corporation",
            )
            generated_license = license_generator.generate_license()

            # Expected license text for Apache License 2.0
            expected_license = (
                "Apache License 2.0\n\nCopyright 2015-2024 Microsoft Corporation.\n\n"
                + "You may use the Software in compliance with the License.\n\n"
                + "You must include a copy of the License in any distribution of the Software."
            )
            # Assert that the generated license matches the expected license
            self.assertEqual(generated_license, expected_license)

    def test_missing_license_file(self):
        """Test handling a missing license file"""
        # Mock an empty license file
        with patch("builtins.open", mock_open(read_data="")):
            # Ensure that a SystemExit exception is raised for a missing
            # license file
            with self.assertRaises(SystemExit):
                license_generator = LicenseGenerator(
                    license_file="nonexistent_license.json",
                    license_type="MIT License",
                    start_year=2015,
                    author="Microsoft Corporation",
                )
                # Attempt to generate the license
                license_generator.generate_license()

    def test_invalid_json_in_license_file(self):
        """Test handling an invalid JSON format in the license file"""
        # Mock an invalid JSON in the license file
        with patch("builtins.open", mock_open(read_data="{invalid json}")):
            # Ensure that a SystemExit exception is raised for invalid JSON
            with self.assertRaises(SystemExit):
                license_generator = LicenseGenerator(
                    license_file="license.json",
                    license_type="MIT License",
                    start_year=2015,
                    author="Microsoft Corporation",
                )
                # Attempt to generate the license
                license_generator.generate_license()

    def test_invalid_license_type(self):
        """Test handling an invalid license type"""
        invalid_license_data = {
            "licenses": {
                "MIT License": {
                    "copyright": ["Copyright {start_year}-{end_year} {author}."],
                    "permissions": ["Permission is hereby granted, free of charge..."],
                    "conditions": ["The above copyright notice..."],
                }
            }
        }
        # Mock license file with invalid license type
        with patch(
            "builtins.open", mock_open(read_data=json.dumps(invalid_license_data))
        ):
            # Ensure that a SystemExit exception is raised for an invalid
            # license type
            with self.assertRaises(SystemExit):
                license_generator = LicenseGenerator(
                    license_file="license.json",
                    license_type="GPL License",  # Invalid license type
                    start_year=2015,
                    author="Microsoft Corporation",
                )
                # Attempt to generate the license
                license_generator.generate_license()


if __name__ == "__main__":
    unittest.main()
