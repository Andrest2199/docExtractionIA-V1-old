import json
import re
from unidecode import unidecode
import tiktoken
import base64


class Utils:
    @classmethod
    def to_dict(self, json_string=str) -> dict:
        """Converts a JSON string to a dictionary with two methods"""
        try:
            if "null" in json_string or "Null" in json_string or "None" in json_string:
                json_string = (
                    json_string.replace("Null", '\\"NA\\"')
                    .replace("null", '\\"NA\\"')
                    .replace("None", '\\"NA\\"')
                )
            json_data = json.loads(str(json_string))
        except Exception as e:
            print(f"Failed to load JSON:{e}, trying to build dictionary...")
            try:
                json_data = self.build_dictionary(str(json_string))
            except Exception as e:
                json_data = json_string
                raise Exception(f"Error: {e}, fail attempting build dictionary...")
        return json_data

    @staticmethod
    def build_dictionary(json_string=str) -> dict:
        new_json = {}
        json_string = str(json_string)
        if json_string.startswith("{") and json_string.endswith("}"):
            json_string = json_string.replace("{", "").replace("}", "")
            json_string = json_string.replace("\n", "").replace("\t", "")
            json_string = json_string.split(",")
            for element in json_string:
                countColon = element.count(":")
                if countColon > 1:
                    element = element.replace(":", "", (countColon - 1))
                temp = element.strip().replace('"', "").split(":")

                if len(temp) > 1:
                    new_json[temp[0]] = (
                        None if temp[1].strip() == "NULL" else temp[1].strip()
                    )
                else:
                    new_json[temp[0]] = None
        else:
            raise ValueError("Input string is not a Valid JSON string")
        new_json = json.dumps(new_json, indent=4, sort_keys=True, ensure_ascii=False)
        return json.loads(new_json)

    @staticmethod
    def decode_text(texto):
        # Decodificamos caracteres UTF-8
        try:
            patron = re.compile(r"\\u([\d\w]{4})")
            final_text = patron.sub(
                lambda x: unidecode(chr(int(x.group(1), 16))), texto
            )
            return final_text
        except Exception as e:
            print(f"Error decoding text: {e}")
            return texto

    @staticmethod
    def read_file(file_path):
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def num_tokens_from_string(string: str, model="gpt-4-vision-preview") -> int:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    @classmethod
    def num_tokens_from_messages(
        self,
        messages,
        model="gpt-3.5-turbo-0125",
    ):
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
            return self.num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            print(
                "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
            )
            return self.num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://platform.openai.com/docs/api-reference for more information of the model."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                if not isinstance(value, dict):
                    num_tokens += len(encoding.encode(value))
                    if key == "name":
                        num_tokens += tokens_per_name
                elif isinstance(value, dict):
                    for k, v in value.items():
                        num_tokens += len(encoding.encode(v))
                        if k == "name":
                            num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|im_start|>assistant<|im_sep|>
        return num_tokens

    def encode_image(image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: The file path '{image_path}' was not found.")
        except PermissionError:
            print(
                f"Error: You do not have permissions to read the file in '{image_path}'."
            )
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


# %%
