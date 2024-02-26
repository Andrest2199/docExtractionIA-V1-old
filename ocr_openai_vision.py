# %% openai vision

import base64
import json
import os
from openai import OpenAI
from utils.json_handler import JsonHandler

# OpenAI API Key
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

# Get base path
# folder_base_path = os.getcwd()

"""
DOCS:
https://platform.openai.com/docs/guides/vision

TODO:
1) Modify prompt to include a few examples of desired output
"""

# %% Encode image


# Define function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def ocr_openai_vision(image_path, output_folder):

    print(f"Processing image: {image_path}")

    # Path to your image
    # image_path = folder_base_path + "/1_image_procesed/0_procesed.jpeg"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Image URL
    image_url = f"data:image/jpeg;base64,{base64_image}"

    # %% Send image to GPT 4 vision
    # Create instance of openAI client
    client = OpenAI()

    # Get response
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # prompt 1
                        # "text": "Return JSON document with the data in this document. Only return ONE JSON not other text"
                        # prompt 2
                        # "text": "Return JSON document with the data in this document. Only return ONE JSON not other text. Consider the following fields: 'unidad_medica_expedidora', 'nivel_atencion', 'delegacion_adscripcion', 'tipo_incapacidad', 'dias_autorizados', 'forma_seguro_enfermedad_general', 'probable_riesgo_trabajo', 'dias_acumulados', 'particion', 'patron', 'numero', 'a_partir_de', 'expedido_el', 'control_maternidad', 'nombre_firma_medico', 'matricula', 'nombre_firma_medico_autoriza', 'matricula_autoriza', 'nota', 'informacion_adicional'",
                        # prompt 3
                        "text": "Create a JSON document with the data in the provided image. Return just ONE json document with all the retrieved fields and format it with underscores on key names and lowercase. ",
                    },
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
        max_tokens=2000,
    )

    # Extract json content from response
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")

    json_data = JsonHandler.to_dict(json_string) 
    file_extension = image_path.split(".")[-1]
    json_file_name = image_path.split("/")[-1].replace(f".{file_extension}", ".json") # add method of ocr

    with open(output_folder + "/" + json_file_name, "w") as file: # call utils function
        json.dump(json_data, file, indent=4)


# %%
