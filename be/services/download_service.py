import os

# Directory for storing temporary files
TEMP_DIR = "tmp"

def get_file_path(filename):
    """
    Returns the full file path if the file exists.
    """
    path = os.path.join(TEMP_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File {filename} not found in {TEMP_DIR}")
    return path
