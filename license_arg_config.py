import argparse
import sys

class LicenseArgConfig:
    def __init__(self):
        """
        Initialize the LicenseArgConfig class, responsible for parsing command-line arguments.
        """
        self.license_file = None
        self.license_type = None
        self.start_year = None
        self.author = None
        self.end_year = None
        self.target_folder = None

    def parse(self):
        """
        Parse command-line arguments using argparse and provide error messages and help information.
        :return: Parsed arguments
        """
        parser = argparse.ArgumentParser(
            description="Generate a license file with the specified parameters."
        )
        
        # Required arguments
        parser.add_argument("--license-file", required=True, help="Path to the license file")
        parser.add_argument("--license-type", required=True, help="Type of the license (e.g., MIT License)")
        parser.add_argument("--start-year", type=int, required=True, help="Start year of the license")
        parser.add_argument("--author", required=True, help="Author of the license")
        
        # Optional argument
        parser.add_argument("--end-year", type=int, help="End year of the license (optional)")
        
        # Target folder argument
        parser.add_argument("--target-folder", required=True, help="Target folder to save the generated file")
        
        try:
            # Parse command-line arguments
            args = parser.parse_args()
            
            # Assign parsed arguments to class attributes
            self.license_file = args.license_file
            self.license_type = args.license_type
            self.start_year = args.start_year
            self.author = args.author
            self.end_year = args.end_year
            self.target_folder = args.target_folder
        except argparse.ArgumentError as e:
            print(f"Error: {e}")
            parser.print_help()
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def display_info(self):
        """Display parsed command-line arguments in the specified order."""
        print(f"License type: {self.license_type}")
        print(f"License file: {self.license_file}")
        print(f"Start year: {self.start_year}")
        print(f"End year: {self.end_year if self.end_year else 'N/A'}")
        print(f"Author: {self.author}")
        print(f"Target folder: {self.target_folder}")


def main():
    # Create LicenseArgConfig instance
    config = LicenseArgConfig()
    
    # Parse command-line arguments
    config.parse()
    
    # Display parsed arguments
    config.display_info()

if __name__ == "__main__":
    main()
