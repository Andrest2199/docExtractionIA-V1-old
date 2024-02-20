# %% openai vision

import base64
import json
import utils
import os
from openai import OpenAI

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
    #Set data for system from folder 'data inject'
    folder_base_path=os.getcwd()
    data_inject = folder_base_path + "/data_inject"

    example_input_doc_1 = os.path.join(data_inject,'1_procesed.jpeg')
    base64_image1 = encode_image(example_input_doc_1)
    example_input_doc_1 =f"data:image/jpeg;base64,{base64_image1}"

    example_json_1 = os.path.join(data_inject,'1_jorge.txt')
    with open(example_json_1) as txt:
        json_1 = txt.read()

    example_input_doc_2 = os.path.join(data_inject,'2_procesed.jpg')
    base64_image2 = encode_image(example_input_doc_2)
    example_input_doc_2 =f"data:image/jpeg;base64,{base64_image2}"

    example_json_2 = os.path.join(data_inject,'2_alejandra.txt')
    with open(example_json_2) as txt2:
        json_2 = txt2.read()
    
    print(f"Processing image: {image_path}")

    # Path to your image
    # image_path = folder_base_path + "/1_image_procesed/0_procesed.jpeg"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    # Image URL
    image_url = f"data:image/jpeg;base64,{base64_image}"
    
    # Create instance of openAI client
    client = OpenAI()

    #Set user prompt
    data_inyection = (
        "You will receive an example image and two examples of text strings extracted from similar documents in d_j_1 and d_j_2 XML tags."
        + "\n"
        + "<d_j_1>"
        + str(json_1)
        + "</d_j_1>"
        + "\n" 
        + "<d_j_2>"
        + str(json_2)
        + "</d_j_2>"
    )  
    print (data_inyection)

    # Set system role
    system_role = {
        "role": "system",
        "content": [{"type":"text",
                     "text":data_inyection},
                    {"type": "image_url", 
                     "image_url": example_input_doc_1}]
    }

    # Get response
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",# gpt-3.5-turbo-0125 #gpt-4-0125-preview
        messages=[system_role,
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
                        "text": "Create a JSON document with the data in the provided image. Return just ONE json document with all the retrieved fields and format it with underscores on key names and lowercase.",
                    },
                    {"type": "image_url", "image_url": image_url}
                ]
            }
        ],
        max_tokens=2000,
    )

    # Extract json content from response
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")

    # Save json data
    print(json_string)
    json_data = json.loads(json_string)
    file_extension = image_path.split(".")[-1]
    json_file_name = image_path.split("/")[-1].replace(f".{file_extension}", ".json")

    with open(output_folder + "/" + json_file_name, "w") as file:
        json.dump(json_data, file, indent=4)

# %% TEST 
folder_base_path=os.getcwd()
image_improved_folder = folder_base_path + "/2_image_improved"
text_extracted_folder = folder_base_path + "/3_text_extracted"

test_file = os.path.join(image_improved_folder,'7_procesed.jpeg')

ocr_openai_vision(test_file, text_extracted_folder)
# %%
