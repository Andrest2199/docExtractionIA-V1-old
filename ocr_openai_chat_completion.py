# %% openai vision
import os
from openai import OpenAI
from utils.utils import Utils
from utils.file_utils import FileUtils


# OpenAI API Key
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

"""
DOCS:
https://platform.openai.com/docs/guides/vision

TODO:
-> text_extracted -> cleaning -> _cleaning 
                  -> ocr_openai_chat.completion.py -> _Complito
"""


# %% Define functions
def chat_completion_cleaning(file_path, output_folder, data_inject_folder, type_doc):
    print(f"Processing text file: {file_path}")
    """
    -> text_extracted -> result 
    Receives the extracted text to process and returns a JSON with the relevant fields.
    """
    # Set Data for system from folder 'Data inject'
    user_prompt = []
    system_prompt = []
    context_data_inyection = ""
    input_results_list = []
    input_txt_list = []
    txt_count = 0
    results_count = 0
    # Retrieve files from 'Data Inject'
    # TODO: En data_inject_folder unir al path el type doc: line 41|ocr_openai_chat_completion.py
    all_data_inject_files = FileUtils.create_list(data_inject_folder)
    for file in all_data_inject_files:
        if file.startswith("result"):
            input_results_list.append(
                FileUtils.read(os.path.join(data_inject_folder, file))
            )
            results_count += 1
        else:
            input_txt_list.append(
                FileUtils.read(os.path.join(data_inject_folder, file))
            )
            txt_count += 1

    # Set context data
    context_data_inyection = f"Here are examples of {txt_count} texts extracted from images and {results_count} result data outputs with relevant fields extract from the text strings delimited by XML tags."

    txt_count = 1
    results_count = 1
    for input_txt, input_result in zip(input_txt_list, input_results_list):
        context_data_inyection += f"\n<example_text_extracted_{txt_count}>{input_txt}</example_text_extracted_{txt_count}>\n<example_result_data_output_{results_count}>{input_result}</example_result_data_output_{results_count}>"
        txt_count += 1
        results_count += 1

    context_data_inyection += f"\nYou will recive a text by the user.Your task is to read and process the text that user provides and return an output dictionary with the relevant fields and format like the next example."
    if type_doc == "IMSS":
        context_data_inyection += '\n"""{\n"DIAS_AUTORIZADOS": STRING,\n"FECHA_APARTIR": DATE STRING,\n"FECHA_EXPEDIDO": DATE STRING,\n"PROBABLE_RIESGO_TRABAJO": SI/NO,\n"RAMO_SEGURO": STRING,\n"SERIE_FOLIO": STRING,\n"TIPO_INCAPACIDAD": STRING\n}"""'
    if type_doc == "INFONAVIT":
        context_data_inyection += '\n"""{\n"TITULO_DOCUMENTO": STRING,\n"CANTIDAD_DE_DESCUENTO": STRING,\n"FECHA": DATE STRING,\n"MOTIVO": ALTA/SUSPENSION,\n"NUMERO_DE_CREDITO": STRING\n}"""'
    if type_doc == "SAT":
        context_data_inyection += '\n"""{\n"CODIGO_POSTAL": NUMBER,\n"CURP": STRING,\n"NOMBRE": STRING,\n"PRIMER_APELLIDO": STRING,\n"SEGUNDO_APELLIDO": STRING,\n"RFC": STRING,\n}"""'

    # Set content system prompt
    system_prompt.append({"type": "text", "text": context_data_inyection})

    # Set user request
    user_prompt.append(
        {
            "type": "text",
            "text": "Create and return a JSON with the next data with all the relevant fields giving priority to those in the desire data output examples.",
        }
    )

    # Set user file request
    # TODO: add try catch
    with open(file_path, encoding="ISO-8859-1") as file:
        user_file = file.read()

    user_prompt.append({"type": "text", "text": user_file})

    # TODO: Numero de tokens usados [guardar]
    # num_tokens = FileUtils.num_tokens_from_messages(user_prompt,"gpt-3.5-turbo-0125")
    # print (f"Tokens in User Prompt: {num_tokens}")
    # num_tokens = FileUtils.num_tokens_from_messages(system_prompt,"gpt-3.5-turbo-0125")
    # print (f"Tokens in System Prompt: {system_prompt}")

    # Create instance of openAI client
    client = OpenAI()

    # Set system role
    system_role = {"role": "system", "content": system_prompt}

    # Get response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",  # gpt-3.5-turbo-0125 #gpt-4-0125-preview, #gpt-4-vision-preview
        messages=[
            system_role,
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=2000,
    )

    # Extract json content from response
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")

    # Save json data
    json_data = Utils.to_dict(json_string)
    file_extension = file_path.split(".")[-1]
    json_file_name = file_path.split("/")[-1].replace(
        f".{file_extension}", ".json"
    )  # add _cleaning or chat or whatever

    tokens_count_by_gpt = response.usage.prompt_tokens
    print(f"Tokens count by API: {tokens_count_by_gpt}")
    return json_data


# %% TEST
# folder_base_path = os.getcwd()

# text_extracted_folder = folder_base_path + "/3_text_extracted"
# results_folder = folder_base_path + "/4_results"
# data_inject_folder = folder_base_path + "/data_inject"

# test_file = os.path.join(
#     text_extracted_folder, "695844 MACIAS LARA JORGE ARMANDO MI909883 ok_HW.txt"
# )
# test_file = os.path.join(text_extracted_folder, "13_test.txt")

# ocr_openai_vision(test_file, results_folder, data_inject_folder)


# %%


# if type(json_string) == dict:
#     json_data = json.loads(json_string)
# elif type(json_string) == str:
#     if json_string.startswith("{") and json_string.endswith("}"):
#         json_string = json_string.replace("{", "[").replace("}", "]")
#         print("after replace", json_string)
#     else:
#         json_string = f"[{json_string}]"
#         print("after concat", json_string)
#     json_string = dict(zip(json_string))
# #     print("after dict", json_string)
# print("cast", str(temp3))


# %%
