import os


def get_all_file_paths(folder_path):
    """
    Get all file paths in a folder, ignoring .DS_Store and .gitignore files
    """
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if not file.endswith((".DS_Store", ".gitignore")):
                file_names.append(file)
    return file_names


def create_file_list(folder_path):
    # Create file name list
    file_name_list = []
    for file_name_original in os.listdir(folder_path):
        # Remove non-ASCII characters
        file_name_original_clean = file_name_original.encode(
            "ascii", errors="ignore"
        ).decode()
        # Append original file name cleaned
        file_name_list.append(file_name_original_clean)
    return file_name_list


def delete_images_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            # Check if it is a file and not a directory and not .gitignore
            if os.path.isfile(file_path) or os.path.islink(file_path):
                if filename != ".gitignore":
                    os.unlink(file_path)  # Unlink (delete) the file
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
