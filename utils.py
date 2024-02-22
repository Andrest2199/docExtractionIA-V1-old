import os
import tiktoken
import base64

def get_all_file_paths(folder_path):
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


def create_file_list(folder_path):
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


def list_text_files(folder_path):
    file_name_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt") or file.endswith(".json"):
            file_name_list.append(file)
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


def save_to_file(file_path_output, str):
    with open(file_path_output, "w") as file:
        file.write(str)


def read_file(file_path):
    with open(file_path) as file:
        return file.read()


def num_tokens_from_string(string: str, model="gpt-4-vision-preview") -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-3.5-turbo-0125",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4-32k-0613",
        "gpt-4-vision-preview",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print(
            "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print(
            "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
        )
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://platform.openai.com/docs/api-reference for more information of the model."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            if type(value) is not dict:
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
            elif type(value) is dict:
                for k, v in value.items():
                    num_tokens += len(encoding.encode(v))
                    if k == "name":
                        num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: El archivo en la ruta '{image_path}' no fue encontrado.")
    except PermissionError:
        print(f"Error: No se tienen permisos para leer el archivo en '{image_path}'.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
