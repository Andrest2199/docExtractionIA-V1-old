import json
import re
from unidecode import unidecode
import tiktoken
import base64
from datetime import datetime


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

    def validate_fields(data):
        if "values" in data.keys() and data["values"] != "":
            fields = data["values"]
        else:
            data["values"] = (
                "Error: No se extrajo ningun campo, favor de validar documento."
            )
            return data

        # Validacion de código postal
        if "CODIGO_POSTAL" in fields:
            if len(fields["CODIGO_POSTAL"]) != 5:
                fields["CODIGO_POSTAL"] = (
                    f"Error: El código postal '{fields['CODIGO_POSTAL']}' es incorrecto."
                )

        # Validacion de CURP
        if "CURP" in fields:
            # Expresión regular para validar el formato de CURP
            patron_CURP = re.compile(r"^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$")

            # Validar el formato de CURP
            if not patron_CURP.match(fields["CURP"]):
                fields["CURP"] = f"Error: El CURP '{fields['CURP']}' es incorrecto."

            # Calcular el dígito verificador
            if "Error" not in fields["CURP"]:
                suma = 0
                diccionario_reemplazo = {
                    "A": "10",
                    "B": "11",
                    "C": "12",
                    "D": "13",
                    "E": "14",
                    "F": "15",
                    "G": "16",
                    "H": "17",
                    "I": "18",
                    "J": "19",
                    "K": "20",
                    "L": "21",
                    "M": "22",
                    "N": "23",
                    "Ñ": "24",
                    "O": "25",
                    "P": "26",
                    "Q": "27",
                    "R": "28",
                    "S": "29",
                    "T": "30",
                    "U": "31",
                    "V": "32",
                    "W": "33",
                    "X": "34",
                    "Y": "35",
                    "Z": "36",
                }
                for i in range(len(fields["CURP"]) - 1):
                    if fields["CURP"][i].isdigit():
                        suma += int(fields["CURP"][i]) * (18 - i)
                    else:
                        suma += int(diccionario_reemplazo[fields["CURP"][i]]) * (18 - i)

                digito_verificador = 10 - (suma % 10)
                if digito_verificador == 10:
                    digito_verificador = 0

                # Verificar el dígito verificador
                if int(fields["CURP"][-1]) != digito_verificador:
                    fields["CURP"] = (
                        f"Error: El dígito verificador del CURP '{fields['CURP']}' es incorrecto."
                    )

        # Validacion de RFC
        if "RFC" in fields:
            # Expresión regular para validar el formato de RFC
            patron_RFC = re.compile(r"^[A-ZÑ]{3,4}[0-9]{6}[A-V0-9]{2}[0-9A]$")

            # Validar el formato de RFC
            if not patron_RFC.match(fields["RFC"]):
                fields["RFC"] = f"Error: El RFC '{fields['RFC']}' es incorrecto."

        # Validacion de Fechas
        for key in fields.keys():
            if "FECHA" in key.upper():
                fecha = fields[key]

                patron_fecha = re.compile(r"\d{2}/\d{2}/\d{2}$")
                if not patron_fecha.match(fecha):
                    fields[key] = (
                        f"Error: El formato de la fecha '{fecha}' es incorrecto."
                    )
                if "Error" not in fields[key]:
                    try:
                        # Dividir la fecha en día, mes y año
                        dia, mes, anio = map(int, fecha.split("/"))

                        # Verificar si el año es válido (en un rango razonable)
                        anio_min = int(str(datetime.today().year)[2:4]) - 5
                        anio_max = int(str(datetime.today().year)[2:4]) + 5
                        if anio < anio_min or anio > anio_max:
                            fields[key] = (
                                f"Error: El año de la fecha '{fecha}' es invalido."
                            )

                        # Verificar si el mes está en el rango de 1 a 12
                        if "Error" not in fields[key]:
                            if mes < 1 or mes > 12:
                                fields[key] = (
                                    f"Error: El mes de la fecha '{fecha}' es invalido."
                                )

                            if "Error" not in fields[key]:
                                # Verificar si el día está en el rango adecuado para cada mes
                                dias_por_mes = [
                                    31,
                                    (
                                        28
                                        if anio % 4 != 0
                                        or (anio % 100 == 0 and anio % 400 != 0)
                                        else 29
                                    ),
                                    31,
                                    30,
                                    31,
                                    30,
                                    31,
                                    31,
                                    30,
                                    31,
                                    30,
                                    31,
                                ]
                                if dia < 1 or dia > dias_por_mes[mes - 1]:
                                    fields[key] = (
                                        f"Error: El día de la fecha '{fecha}' es invalido."
                                    )

                    except ValueError:
                        fields[key] = f"Error: La fecha '{fecha}' es invalida."
        print("Fields validated.")
        return fields
