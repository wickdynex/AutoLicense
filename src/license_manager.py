import os
from license_generator import LicenseGenerator

class LicenseManager:
    def __init__(self, license_text: str):
        """
        Initialize the LicenseManager instance
        :param license_text: The license text to be added to the file
        """
        self.license_text = license_text

    def check_and_add_license(self, file_path: str):
        """
        Check if the file already contains a license. If not, add the license.
        :param file_path: The path to the file where the license should be added
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return

        # Check if the file already contains the license
        with open(file_path, 'r') as file:
            content = file.read()

            if self.license_text in content:
                print(f"License already exists in {file_path}. No changes made.")
                return

        # Determine the comment style based on the file extension
        file_extension = os.path.splitext(file_path)[1]

        # Files that use `#` for comments (Single-line comments)
        if file_extension in ['.py', '.sh', '.txt', '.rb', '.pl', '.lua', '.bash', '.zsh', '.r', '.yml']:  
            comment_style = '# '
        # Files that use `/* ... */` for comments (Multi-line comments)
        elif file_extension in ['.java', '.cpp', '.h', '.js', '.css', '.m', '.swift', '.ts', '.go', '.c']:  
            comment_style = '/* '
        # Files that use `<!-- -->` for line comments (like XML, HTML)
        elif file_extension in ['.xml', '.html', '.xhtml', '.md']:
            comment_style = '<!-- '
        else:
            # If the file type is unsupported, print a warning
            print(f"Warning: File type {file_extension} not recognized, skipping...")
            return

        # Format the license text with the correct comment style
        license_with_comment = self.format_license_with_comments(comment_style)

        # Add the formatted license text at the beginning of the file
        with open(file_path, 'r+') as file:
            original_content = file.read()
            file.seek(0, 0)  # Move the file pointer to the beginning
            file.write(license_with_comment + "\n" + original_content)

        print(f"License added successfully to {file_path}.")

    def format_license_with_comments(self, comment_style: str) -> str:
        """
        Format the license text with the appropriate comment style
        :param comment_style: The comment style, either `# `, `/* */`, or `<!-- -->`
        :return: The formatted license text
        """
        lines = self.license_text.split("\n")
        formatted_lines = []

        if comment_style == '# ':
            # Single-line comment style: start each line with `# `
            full_license = "\n".join([f"{comment_style}{line}" for line in lines])
        elif comment_style == '/* ':
            # Multi-line comment style: start with `/*` and end with `*/`
            formatted_lines.append("/*")
            for line in lines:
                formatted_lines.append(f" * {line}")
            formatted_lines.append(" */")
            full_license = "\n".join(formatted_lines)
        elif comment_style == '<!-- ':
            # Line comment style for HTML/XML: use `<!--` and `-->`
            formatted_lines.append("<!--")
            for line in lines:
                formatted_lines.append(f" {line}")
            formatted_lines.append("-->")
            full_license = "\n".join(formatted_lines)
        
        return full_license

# Main function to test LicenseManager and LicenseGenerator
if __name__ == "__main__":
    # Use LicenseGenerator to generate the license text
    license_generator = LicenseGenerator(
        license_file="data/license.json",  # Assume license.json is located in the data folder
        license_type="MIT License",
        start_year=2015,
        end_year=2024,
        author="Microsoft Corporation"
    )

    # Generate the license text
    license_text = license_generator.generate_license()

    # Create a LicenseManager instance with the generated license text
    license_manager = LicenseManager(license_text)

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
