import os


class FileUtils:
    @staticmethod
    def get_paths(folder_path, depth=1):
        """
        Get all file paths in a folder up to a certain depth, ignoring .DS_Store and .gitignore files
        parameters:
            folder_path: str - path to the folder
            depth: int (default=1) - depth of the folder to search
        """
        file_paths = []
        for root, dirs, files in os.walk(folder_path):
            if root.count(os.sep) - folder_path.count(os.sep) < depth:
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
                # "ascii", errors="ignore"
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

    @staticmethod
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

    @staticmethod
    def save(file_path_output, data):
        if isinstance(data, str):
            with open(file_path_output, "w") as file:
                file.write(data)
        else:
            with open(file_path_output, "wb") as file:
                file.write(data)
        return file_path_output

    @staticmethod
    def get_original_names(input_folder_path):
        # Create data dictionary and extract original file name
        file_name_list = FileUtils.create_list(input_folder_path)
        data = {}
        for ii, file_name_original in enumerate(file_name_list):
            if file_name_original not in [".gitignore", ".DS_Store"]:
                data[str(ii)] = {"file_name_original": file_name_original}
        return data

    @staticmethod
    def read(file_path):
        with open(file_path) as file:
            return file.read()
