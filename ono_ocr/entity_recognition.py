# %% openai chat completions

import os
from openai import OpenAI
from utils.utils import Utils
from utils.file_utils import FileUtils
from django.conf import settings

# OpenAI API Key
api_key = settings.OPENAI_API_KEY


def chat_completions_entity_extraction(
    extracted_text, data_inject_folder, type_doc
) -> dict:
    """
    -> text_extracted -> result
    Receives the extracted text to process and returns a JSON with the relevant fields.
    """
    # Set Data for system from folder 'Data inject'
    context_data_inyection = ""
    input_results_list = []
    input_txt_list = []
    txt_count = 0
    results_count = 0
    all_data_inject_files = []
    # Retrieve files from 'Data Inject'
    if type_doc == "IMSS":
        data_inject_sub_folder = os.path.join(data_inject_folder, "IMSS")
        all_data_inject_files = FileUtils.get_paths(data_inject_sub_folder, 2)
    elif type_doc == "INFONAVIT":
        data_inject_sub_folder = os.path.join(data_inject_folder, "INFONAVIT")
        all_data_inject_files = FileUtils.get_paths(data_inject_sub_folder, 2)
    elif type_doc == "SAT":
        data_inject_sub_folder = os.path.join(data_inject_folder, "SAT")
        all_data_inject_files = FileUtils.get_paths(data_inject_sub_folder, 1)
    else:
        raise ValueError(
            "Document type not recognized. Please provide a valid document type: IMSS, INFONAVIT, SAT"
        )

    for file in all_data_inject_files:
        file_name = os.path.basename(file)
        if file_name.startswith("result"):
            input_results_list.append(FileUtils.read(file))
            results_count += 1
        elif file_name.startswith("data"):
            input_txt_list.append(FileUtils.read(file))
            txt_count += 1
        else:
            print(f"File {file} not recognized")

    # Set context data
    context_data_inyection = f"Your role is to extract relevant information from raw text. In between XML tags you will find {txt_count} examples of raw text inputs and information extracted outputs with the relevant entities to be recognized. \n\n"

    txt_count = 1
    results_count = 1
    for input_txt, input_result in zip(input_txt_list, input_results_list):
        context_data_inyection += f"<raw_text_input_example_{txt_count}>\n\n{input_txt}\n\n</raw_text_input_example_{txt_count}>\n\n<information_extracted_output_example_{results_count}>\n\n{input_result}\n\n</information_extracted_output_example_{results_count}>\n\n"
        txt_count += 1
        results_count += 1

    context_data_inyection += "\nYou will recive a new raw text by the user. Your task is to analyse the raw text, recognize the entities to be extracted, and create a JSON with the relevant entities. Use the following format for the output JSON:\n\n"
    if type_doc == "IMSS":
        context_data_inyection += """
    {
        "SERIE_Y_FOLIO": STRING,
        "TIPO_INCAPACIDAD": STRING,
        "RAMO_DE_SEGURO": STRING,
        "PROBABLE_RIESGO_TRABAJO": STRING,
        "DIAS_AUTORIZADOS": STRING,
        "FECHA_A_PARTIR": DATE STRING,
        "FECHA_EXPEDIDO": DATE STRING,
        "NUMERO_DE_SEGURIDAD_SOCIAL": STRING,
        "CURP": STRING,
        "NOMBRE_DEL_ASEGURADO": STRING,
        "CLAVE_PATRONAL": STRING,
        "NOMBRE_DEL_PATRON": STRING
    }
    """
    if type_doc == "INFONAVIT":
        context_data_inyection += """
    {
        "TITULO": STRING,
        "FOLIO": STRING,
        "FECHA_EMISION": DATE STRING,
        "FECHA_RECEPCION": DATE STRING,
        "NUMERO_DE_CREDITO": STRING,
        "DESCUENTO": STRING,
        "RFC":STRING,
        "NUMERO_DE_SEGURIDAD_SOCIAL": STRING,
        "RFC_PATRON": STRING,
        "NUMERO_DE_REGISTRO_PATRONAL": STRING,
        "RAZON_SOCIAL": STRING
    }
    """
        # "SELLO": TRUE/FALSE,
    if type_doc == "SAT":
        context_data_inyection += """
    {
        "CODIGO_POSTAL": NUMBER,
        "CURP": STRING,
        "NOMBRES": STRING,
        "PRIMER_APELLIDO": STRING,
        "SEGUNDO_APELLIDO": STRING,
        "RFC": STRING,
        "ESTATUS_EN_EL_PADRON": STRING
    }
    """
    # Set system role
    system_content = {"role": "system", "content": context_data_inyection}

    user_content = {"role": "user", "content": extracted_text}

    # Create instance of openAI client
    client = OpenAI(api_key=api_key)

    # Get response
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",  # gpt-3.5-turbo-0125 #gpt-4-0125-preview, #gpt-4-vision-preview
        messages=[
            system_content,
            user_content,
        ],
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    # Extract json content from response
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")

    # Return json data
    json_data = Utils.to_dict(json_string)

    tokens_count_by_gpt = response.usage.prompt_tokens

    return json_data
