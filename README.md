<!--
 MIT License
 
 Copyright (c) 2024 - 2024 Wick Dynex
 
 Permission is hereby granted, free of charge,
 to any person obtaining a copy of this software and associated documentation files (the 'Software'),
 to deal in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software
 and to permit persons to whom the Software is furnished to do so
 
 The above copyright notice
 and this permission notice
 shall be included in all copies or substantial portions of the Software.
-->
# AutoLicense

> Language: [中文 README](README_zh.md)

a python tool to automatically add license headers to source files in a target directory. it generates the license header based on user-specified parameters, formats it according to file type, and only adds it if missing.

## Features

- **Automatic License Header Insertion**: Adds a customizable license header to supported files in the target directory.
- **License Text Generation**: Constructs the license text dynamically based on input parameters (e.g., license type, author, start year).
- **File Type Detection**: Automatically detects the file type (e.g., Python, Java, C++) and applies the appropriate comment style.
- **License Presence Check**: Checks if a license header is already present and avoids duplicating it.
- **Batch Processing**: Supports adding license headers to multiple files in a directory at once.

## Requirements

- Python 3.x

## Usage

Run the script with the following command to add license headers to all supported files in a target folder:

```bash
python main.py  --license-file=LICENSE_FILE 
                --license-type=LICENSE_TYPE 
                --start-year=START_YEAR
                --author=AUTHOR 
                --target-folder=TARGET_FOLDER 
                [--end-year=END_YEAR] 
                [--detail]
```

## Command-Line Arguments

The following arguments are required for proper functioning of the tool:

- `--license-file=LICENSE_FILE`:  
  Description: Path to the `.json` license file (e.g., `data/license.json`).  
  Note: The JSON file must contain the license type(s) to be added.

- `--license-type=LICENSE_TYPE`:  
  Description: Specifies the license type to be added. The license must be defined in the provided `.json` file (e.g., `MIT License`, `Apache License 2.0`).  
  Note: The license type must exist in the JSON file's "licenses" object.

- `--start-year=START_YEAR`:  
  Description: The start year for the license header (e.g., `2024`).  
  Note: This is a required argument and must be less than or equal to `--end-year`.

- `--end-year=END_YEAR`:  
  Description: The end year for the license header (optional). 
  Note: If not specified, the `end-year` is assumed to be the current year.

- `--author=AUTHOR`:  
  Description: The name of the author or organization (e.g., "John Wick").  
  Note: This is a required argument.

- `--target-folder=TARGET_FOLDER`:  
  Description: The path to the directory or file where the license header needs to be added.  
  Note: This must be a valid and writable directory or file path.

- `--detail`:  
  Description: If included, it provides detailed output showing what files were modified and the license text that was added.  
  Default: The output is concise by default (i.e., without details).

## Example

### Example Usage

To run the script and add a license header to the files in the target folder, use the following command:

```bash
python main.py  --license-file="data/license.json" 
                --license-type="MIT License"
                --start-year=1998 
                --end-year=2023 
                --author="John Wick" 
                --target-folder="./folder"
```

### Expected Output

```bash
License file: data/license.json
License type: MIT License
Start year: 1998
End year: 2023
Author: John Wick
Target folder: ./folder
Show details: False
```

## License

 - This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).