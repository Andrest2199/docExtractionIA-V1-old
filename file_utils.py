import os


class FileUtils:
    @staticmethod
    def get_paths(folder_path):
        """
        Get all file paths in a folder, ignoring .DS_Store and .gitignore files
        """
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if ".DS_Store" not in file and ".gitignore" not in file:
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        return file_paths

    @staticmethod
    def create_list(folder_path):
        """
        Get all file names in a folder, ignoring .DS_Store and .gitignore files
        """
        # Create file name list
        file_name_list = []
        for file_name_original in os.listdir(folder_path):
            # Remove non-ASCII characters
            file_name_original_clean = file_name_original.encode(
                "ascii", errors="ignore"
            ).decode()
            # Append original file name cleaned
            if not file_name_original.endswith((".DS_Store", ".gitignore", ".json")):
                file_name_list.append(file_name_original_clean)
        return file_name_list

    @staticmethod
    def list_text_files(folder_path):
        file_name_list = []
        for file in os.listdir(folder_path):
            if file.endswith(".txt") or file.endswith(".json"):
                file_name_list.append(file)
        return file_name_list

    def delete_from_folder(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Check if it is a file and not a directory and not .gitignore
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if filename != ".gitignore":
                        os.unlink(file_path)  # Unlink (delete) the file
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def save(file_path_output, str):
        with open(file_path_output, "w") as file:
            file.write(str)

    def get_original_names(input_folder_path):
        file_name_list = []
        for file_name_original in os.listdir(input_folder_path):
            if file_name_original != ".gitignore" and file_name_original != ".DS_Store":
                file_name_list.append(file_name_original)
        return file_name_list
