import os
from enum import Enum
from datetime import datetime
from src.license_generator import LicenseGenerator

class CommentStyle(Enum):
    """ Enum to map file extensions to their respective comment styles. """
    SINGLE_LINE = "# "  # For single-line comments
    MULTI_LINE = "/* "  # For multi-line comments (start with /*, end with */)
    XML_HTML = "<!-- "  # For HTML/XML comments (start with <!--, end with -->)

class FileType(Enum):
    """ Enum to map file extensions to their respective comment styles. """
    PYTHON = ('.py', CommentStyle.SINGLE_LINE)
    SHELL = ('.sh', CommentStyle.SINGLE_LINE)
    TEXT = ('.txt', CommentStyle.SINGLE_LINE)
    RUBY = ('.rb', CommentStyle.SINGLE_LINE)
    PERL = ('.pl', CommentStyle.SINGLE_LINE)
    LUA = ('.lua', CommentStyle.SINGLE_LINE)
    BASH = ('.bash', CommentStyle.SINGLE_LINE)
    ZSH = ('.zsh', CommentStyle.SINGLE_LINE)
    R = ('.r', CommentStyle.SINGLE_LINE)
    TOML = ('.toml', CommentStyle.SINGLE_LINE)
    YAML = ('.yml', CommentStyle.SINGLE_LINE)
    JAVA = ('.java', CommentStyle.MULTI_LINE)
    CPP = ('.cpp', CommentStyle.MULTI_LINE)
    C = ('.c', CommentStyle.MULTI_LINE)
    HEADER = ('.h', CommentStyle.MULTI_LINE)
    JAVASCRIPT = ('.js', CommentStyle.MULTI_LINE)
    CSS = ('.css', CommentStyle.MULTI_LINE)
    HTML = ('.html', CommentStyle.XML_HTML)
    XML = ('.xml', CommentStyle.XML_HTML)
    MD = ('.md', CommentStyle.XML_HTML)
    
    def __init__(self, extension, comment_style):
        self.extension = extension
        self.comment_style = comment_style

class LicenseKeyword(Enum):
    """ Enum to store common keywords in license text """
    COPYRIGHT = "Copyright"
    LICENSE = "License"
    YEAR = str(datetime.now().year)  # Get the current year dynamically

class LicenseManager:
    def __init__(self, license_text: str, detail: bool = False):
        """
        Initialize the LicenseManager instance
        :param license_text: The license text to be added to the file
        :param detail: A flag to control whether detailed logs should be printed
        """
        self.license_text = license_text
        self.detail = detail  

    def check_and_add_license(self, file_path: str):
        """
        Check if the file already contains a license. If not, add the license.
        :param file_path: The path to the file where the license should be added
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return

        # Check if the file already contains the license in the beginning (can be more sophisticated)
        with open(file_path, 'r') as file:
            content = file.read()

            if self.is_license_present(content):
                self.print_log(f"License already exists in {file_path}. No changes made.")
                return

        # Determine the comment style based on the file extension
        file_extension = os.path.splitext(file_path)[1]

        # Find the matching file type based on extension
        file_type = self.get_file_type(file_extension)
        
        if not file_type:
            self.print_log(f"Warning: File type {file_extension} not recognized, skipping...")
            return

        # Get the comment style associated with this file type
        comment_style = file_type.comment_style.value

        # Format the license text with the correct comment style
        license_with_comment = self.format_license_with_comments(comment_style)

        # Add the formatted license text at the beginning of the file
        with open(file_path, 'r+') as file:
            original_content = file.read()
            file.seek(0, 0)  # Move the file pointer to the beginning
            file.write(license_with_comment + "\n" + original_content)

        self.print_log(f"License added successfully to {file_path}.")

    def is_license_present(self, content: str) -> bool:
        """
        Check if the content already contains a license at the beginning of the file.
        :param content: The content of the file
        :return: True if the license is found, otherwise False
        """
        # Normalize the content: remove leading/trailing spaces, line breaks, etc.
        content = content.strip().lower()  # Convert content to lowercase

        # Check if any of the license-related keywords exist in the content
        for keyword in LicenseKeyword:
            if keyword.value.lower() in content:  # Compare using lowercase
                return True
        return False

    def get_file_type(self, file_extension: str) -> FileType:
        """Returns the appropriate FileType enum based on the file extension."""
        for file_type in FileType:
            if file_extension == file_type.extension:
                return file_type
        return None

    def format_license_with_comments(self, comment_style: str) -> str:
        """
        Format the license text with the appropriate comment style
        :param comment_style: The comment style, either '#' , '/* */', or '<!-- -->'
        :return: The formatted license text
        """
        lines = self.license_text.split("\n")
        formatted_lines = []

        if comment_style == CommentStyle.SINGLE_LINE.value:
            # Single-line comment style: start each line with '#' 
            full_license = "\n".join([f"{comment_style}{line}" for line in lines])
        elif comment_style == CommentStyle.MULTI_LINE.value:
            # Multi-line comment style: start with '/*' and end with '*/'
            formatted_lines.append("/*")
            for line in lines:
                formatted_lines.append(f" * {line}")
            formatted_lines.append(" */")
            full_license = "\n".join(formatted_lines)
        elif comment_style == CommentStyle.XML_HTML.value:
            # Line comment style for HTML/XML: use '<!--' and '-->'
            formatted_lines.append("<!--")
            for line in lines:
                formatted_lines.append(f" {line}")
            formatted_lines.append("-->")
            full_license = "\n".join(formatted_lines)
        
        return full_license

    def print_log(self, message: str):
        """ Prints the log message only if the detail flag is set to True """
        if self.detail:
            print(f"[INFO] {message}")


# Main function to test LicenseManager and LicenseGenerator
if __name__ == "__main__":
    # Use LicenseGenerator to generate the license text
    license_generator = LicenseGenerator(
        license_file="data/license.json",  # Assume license.json is located in the data folder
        license_type="MIT License",
        start_year=2015,
        end_year=datetime.now().year,  # Use current year dynamically
        author="Microsoft Corporation"
    )

    # Generate the license text
    license_text = license_generator.generate_license()

    # Create a LicenseManager instance with the generated license text and detail flag set to True
    license_manager = LicenseManager(license_text, detail=True)

    # Test with various file paths in /test/testfile/
    file_paths = [
        "test/testfile/test.cpp",   # Test with .cpp file
        "test/testfile/test.java",  # Test with .java file
        "test/testfile/test.py",    # Test with .py file
        "test/testfile/test.txt",   # Test with .txt file
        "test/testfile/test.html",  # Test with .html file
        "test/testfile/test.c",     # Test with .c file
        "test/testfile/test.r",     # Test with .r file
        "test/testfile/test.js",    # Test with .js file
        "test/testfile/test.sh",    # Test with .sh file
        "test/testfile/test.css",   # Test with .css file
        "test/testfile/test.h",     # Test with .h file
        "test/testfile/test.xml",   # Test with .xml file
        "test/testfile/test.md",    # Test with .md file
        "test/testfile/test.json",  # Test with .json file
        "test/testfile/test.yml",   # Test with .yml file
        "test/testfile/test.toml"   # Test with .toml file
    ]

    # Iterate through each file and add the license
    for file_path in file_paths:
        print(f"\nChecking and adding license to {file_path}...")
        license_manager.check_and_add_license(file_path)

    license_manager.detail = False

    for file_path in file_paths:
        print(f"\nChecking and adding license to {file_path}...")
        license_manager.check_and_add_license(file_path)
