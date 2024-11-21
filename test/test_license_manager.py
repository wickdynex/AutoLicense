import unittest
from unittest.mock import patch, mock_open
from src.license_manager import LicenseManager, LicenseKeyword, FileType, CommentStyle
from datetime import datetime


class TestLicenseManager(unittest.TestCase):
    @patch("os.path.exists")
    def test_check_and_add_license_file_not_exist(self, mock_exists):
        # Simulate the file does not exist
        mock_exists.return_value = False
        
        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Test with a non-existent file path
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/non_existent.py")
            mock_print.assert_called_with("Error: The file test/testfile/non_existent.py does not exist.")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="MIT License\nCopyright 2015-2024 Microsoft Corporation")
    def test_check_and_add_license_already_exists(self, mock_file, mock_exists):
        # Simulate that the file exists and already contains a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Simulate that the file already contains a license
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/existing_license.py")
            mock_print.assert_called_with("[INFO] License already exists in test/testfile/existing_license.py. No changes made.")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file.\n")
    def test_check_and_add_license_add_license(self, mock_file, mock_exists):
        # Simulate that the file exists, but does not contain a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Check adding a license to a file without one
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/new_file.py")

            # Check that the license was added successfully
            mock_print.assert_called_with("[INFO] License added successfully to test/testfile/new_file.py.")

            # Verify that the file content includes the correct comment format
            handle = mock_file()
            handle.seek.assert_called_once_with(0, 0)  # The file pointer should move to the beginning

            # Here you can check if the written data adheres to the required format
            written_data = handle.write.call_args[0][0]
            self.assertTrue(written_data.startswith("# MIT License"))  # Assuming single-line comments

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file.\n")
    def test_check_and_add_license_multi_line_comment(self, mock_file, mock_exists):
        # Simulate that the file exists, but does not contain a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation\n"
        license_manager = LicenseManager(license_text, detail=True)

        # Test a .cpp file, which should use multi-line comments
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/test.cpp")

            # Check that the license was added successfully
            mock_print.assert_called_with("[INFO] License added successfully to test/testfile/test.cpp.")

            # Check if the written license adheres to multi-line comment format
            mock_file.assert_called_with("test/testfile/test.cpp", 'r+')
            handle = mock_file()
            written_data = handle.write.call_args[0][0]
            print(written_data)
            self.assertTrue(written_data.startswith("/*"))  # Multi-line comments should start with '/*'
            self.assertTrue(written_data.endswith("\n"))  # Multi-line comments should end with '*/'

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="This is a test file.\n")
    def test_check_and_add_license_html_comment(self, mock_file, mock_exists):
        # Simulate that the file exists, but does not contain a license
        mock_exists.return_value = True

        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Test an .html file, which should use HTML comments
        with patch("builtins.print") as mock_print:
            license_manager.check_and_add_license("test/testfile/test.html")

            # Check that the license was added successfully
            mock_print.assert_called_with("[INFO] License added successfully to test/testfile/test.html.")

            # Check if the written license adheres to HTML comment format
            handle = mock_file()
            written_data = handle.write.call_args[0][0]
            self.assertTrue(written_data.startswith("<!--"))  # HTML comments should start with '<!--'
            self.assertTrue(written_data.endswith("\n"))  # HTML comments should end with '-->'

    def test_is_license_present(self):
        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Test when the file content contains the license
        content_with_license = "MIT License\nCopyright 2015-2024 Microsoft Corporation\nSome more content"
        self.assertTrue(license_manager.is_license_present(content_with_license))

        # Test when the file content does not contain the license
        content_without_license = "Some random content here."
        self.assertFalse(license_manager.is_license_present(content_without_license))

    def test_get_file_type(self):
        # Test the mapping of different file types
        license_manager = LicenseManager("MIT License\nCopyright 2015-2024 Microsoft Corporation", detail=True)

        # Test known file extensions
        self.assertEqual(license_manager.get_file_type('.cpp'), FileType.CPP)
        self.assertEqual(license_manager.get_file_type('.html'), FileType.HTML)

        # Test unknown file extension
        self.assertIsNone(license_manager.get_file_type('.unknown'))

    def test_format_license_with_comments(self):
        license_text = "MIT License\nCopyright 2015-2024 Microsoft Corporation"
        license_manager = LicenseManager(license_text, detail=True)

        # Test single-line comments
        formatted = license_manager.format_license_with_comments(CommentStyle.SINGLE_LINE.value)
        self.assertTrue(formatted.startswith("# MIT License"))
        self.assertTrue(formatted.endswith("# Copyright 2015-2024 Microsoft Corporation"))

        # Test multi-line comments
        formatted = license_manager.format_license_with_comments(CommentStyle.MULTI_LINE.value)
        self.assertTrue(formatted.startswith("/*"))
        self.assertTrue(formatted.endswith(" */"))

        # Test XML/HTML comments
        formatted = license_manager.format_license_with_comments(CommentStyle.XML_HTML.value)
        self.assertTrue(formatted.startswith("<!--"))
        self.assertTrue(formatted.endswith("-->"))


if __name__ == "__main__":
    unittest.main()
