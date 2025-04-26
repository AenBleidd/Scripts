import os
import re
import sys

import zipfile

def rename_zip_files_in_directory(directory: str) -> None:
    for zip_filename in os.listdir(directory):
        if zip_filename.endswith('.zip'):
            print(f"Processing: {zip_filename}")
            match = re.search(r'linux-package_(manager|client)_(.*)_\.zip', zip_filename)
            if match:
                os_name = match.group(2)
                with zipfile.ZipFile(os.path.join(directory, zip_filename), 'r') as zip_ref:
                    if len(zip_ref.filelist) == 1:
                        filename = zip_ref.filelist[0].filename
                        zip_ref.extractall(directory)
                        name, ext = os.path.splitext(filename)
                        if (ext == '.rpm'):
                            os.rename(os.path.join(directory, filename), os.path.join(directory, f"{name}.{os_name}.rpm"))
                        elif (ext == '.deb'):
                            os.rename(os.path.join(directory, filename), os.path.join(directory, f"{name}_{os_name}.deb"))
                        else:
                            print(f"Error: {filename} is not a valid file type.")
                            break
                    else:
                        print(f"Error: {zip_filename} contains multiple files.")
                        break
            else:
                print(f"Error: {zip_filename} does not match the expected pattern.")
                break
        os.remove(os.path.join(directory, zip_filename))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python RenameBOINCLinuxPackages.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        sys.exit(1)

    rename_zip_files_in_directory(directory)
