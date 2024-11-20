import os
import argparse

def add_license_header(file_path, header_text):
    with open(file_path, 'r+') as f:
        content = f.read()
        if header_text not in content:
            f.seek(0, 0)
            f.write(header_text + '\n' + content)

def process_directory(directory, header_text):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.js') or file.endswith('.py'):  # 可以根据需求扩展文件类型
                add_license_header(os.path.join(root, file), header_text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add license header to files.')
    parser.add_argument('directory', type=str, help='The directory to process.')
    parser.add_argument('header', type=str, help='The license header to add.')
    args = parser.parse_args()

    process_directory(args.directory, args.header)
