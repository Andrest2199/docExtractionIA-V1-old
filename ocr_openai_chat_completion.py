# %% openai vision
import json
from utils.file_utils import FileUtils
import os
from openai import OpenAI
from utils.json_handler import JsonHandler
import re

# OpenAI API Key
OpenAI.api_key = os.environ["OPENAI_API_KEY"]

"""
DOCS:
https://platform.openai.com/docs/guides/vision

TODO:
-> text_extracted -> cleaning -> _cleaning 
                  -> ocr_openai_chat.completion.py -> _Complito
1) Modify prompt to include a few examples of desired output
2) Modify parameter to detect wich type of document is, so the data correspond to it.
3) Add bank of results for SAT and INFONAVIT
"""


# %% Define functions
def chat_completion_cleaning(file_path, output_folder, data_inject_folder):
    """
    -> text_extracted -> result 
    Receives the extracted text to process and returns a JSON with the relevant fields.
    IMSS
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
    #IMSS context data
    context_data_inyection += '\n"""{\n"DIAS_AUTORIZADOS": STRING,\n"FECHA_APARTIR": DATE STRING,\n"FECHA_EXPEDIDO": DATE STRING,\n"PROBABLE_RIESGO_TRABAJO": SI/NO,\n"RAMO_SEGURO": STRING,\n"SERIE_FOLIO": STRING,\n"TIPO_INCAPACIDAD": STRING\n}"""'
    
    # TODO: add context_data
    # Set content system prompt
    system_prompt.append({"type": "text", "text": context_data_inyection})

    print(f"Processing text file: {file_path}")
    # Set user request
    user_prompt.append(
        {
            "type": "text",
            "text": "Create and return a JSON with the next data with all the relevant fields giving priority to those in the desire data output examples.",
        }
    )

    # Set user file request

    with open(file_path, encoding='ISO-8859-1') as file:
        user_file = file.read()
        
    user_prompt.append({"type": "text", "text": user_file})

    # TODO: Numero de tokens usados [guardar]
    # num_tokens = FileUtils.num_tokens_from_messages(user_prompt,"gpt-3.5-turbo-0125")
    # print (f"Tokens in User Prompt: {num_tokens}")
    # num_tokens = FileUtils.num_tokens_from_messages(system_prompt,"gpt-3.5-turbo-0125")
    # print (f"Tokens in System Prompt: {system_prompt}")

    # print(f"Final User Prompt: {json.dumps(user_prompt,ensure_ascii=False,indent=2)}")
    # print(f"Final System Prompt: {json.dumps(system_prompt,ensure_ascii=False,indent=2)}")

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
    json_data = JsonHandler.to_dict(json_string)
    file_extension = file_path.split(".")[-1]
    json_file_name = file_path.split("/")[-1].replace(
        f".{file_extension}", ".json"
    )  # add _cleaning or chat or whatever
    # TODO: call function to open
    with open(output_folder + "/" + json_file_name + "_completion", "w") as file:
        json.dump(json_data, file, indent=4)

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
json_string = '{\n\t "DIAS_AUTORIZADOS": "SIETE",\n\t "FECHA_APARTIR": "A PARTIR DEL EXPEDIDO",\n\t "FECHA_EXPEDIDO": "SIG",\n\t "PROBABLE_RIESGO_TRABAJO": "NO",\n\t "RAMO_SEGURO": "ENFERMEDAD GENERAL",\n\t "SERIE_FOLIO": "KEUI", \n\t "TIPO_INCAPACIDAD"\n}'


# %%
