import os

def find_file(directory, target_filename):
    """Find target file

    Args:
        directory (str): directory to be found
        target_filename (_type_): target file


    Returns:
        str: Returns the name of the file in the directory if there is one, or None if there isn't.
    """
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file() and os.path.splitext(entry.name)[0] == os.path.splitext(target_filename)[0]:
                return entry.name
    return None