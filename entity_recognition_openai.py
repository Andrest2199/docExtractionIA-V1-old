# %% entity recognition openAI

#TODO: Discharge/Delete class... 
import json
from openai import OpenAI
import os
from utils.json_handler import JsonHandler

"""
DOCUMENTATION
https://platform.openai.com/docs/api-reference/chat/create
https://platform.openai.com/docs/guides/entity-recognition


SYSTEM CONTENT = 
A continuacion recibiras varios ejemplos de texto input para procesar y un diccionario output con los 
campos que necesitamos extraer delimitados por html tags. Tu tarea es procesar el texto input 
y devolver un diccionario output con los siguientes campos y formatos:

{    
    "DIAS_AUTORIZADOS": string,
    "FECHA_APARTIR": date string,
    "FECHA_EXPEDIDO": date string,
    "PROBABLE_RIESGO_TRABAJO": SI / NO,
    "RAMO_SEGURO": string,
    "SERIE_FOLIO": string,
    "TIPO_INCAPACIDAD": string
}

<texto_string_input_1>

text_string_one

</texto_string_input_1>

<dictionary_output_1>

dictionary_one

</dictionary_output_1>

<texto_string_input_2>

text_string_two

</texto_string_input_2>

<dictionary_output_2>

dictionary_two

</dictionary_output_2>

<texto_string_input_3>

text_string_three

</texto_string_input_3>

<dictionary_output_3>

dictionary_three

</dictionary_output_1>

"""

# dictionary_1 = {
#         "DIAS_AUTORIZADOS": "SETE",
#         "FECHA_APARTIR": "06/11/2023",
#         "FECHA_EXPEDIDO": "08/11/2023",
#         "PROBABLE_RIESGO_TRABAJO": "NO",
#         "RAMO_SEGURO": "ENFERMEDAD GENERAL",
#         "SERIE_FOLIO": "VZ948810",
#         "TIPO_INCAPACIDAD": "INICIAL",
#     }


# %%
def recognition_openai(
    text_extracted_1,
    text_extracted_2,
    text_extracted_3,
    dictionary_one,
    dictionary_2,
    dictionary_3,
    unseen_text,
):
    """
    IMSS
    text extracted -> dic_result
    text_string_one-> aws_extract
    text_string_two-> google_vision_extract
    """

    instruccion = f"A continuacion recibiras varios ejemplos de texto input para procesar y un diccionario output con los campos que necesitamos extraer delimitados por html tags. Tu tarea es procesar el texto input y devolver un JSON con los siguientes campos y formatos:"

    ejemplo_output = f'DIAS_AUTORIZADOS": string, "FECHA_APARTIR": date string, "FECHA_EXPEDIDO": date string, "PROBABLE_RIESGO_TRABAJO": SI / NO, "RAMO_SEGURO": string, "SERIE_FOLIO": string, "TIPO_INCAPACIDAD": string'

    text_string_one = text_extracted_1

    text_string_two = text_extracted_2
    dictionary_two = dictionary_2
    text_string_three = text_extracted_3
    dictionary_three = dictionary_3

    system_content = f"{instruccion}{ejemplo_output}/n/n<texto_string_input_ejemplo_1>/n/n{text_string_one}/n/n</texto_string_input_ejemplo_1>/n/n<dictionary_output_ejemplo_1>/n/n{dictionary_one}/n/n</dictionary_output_ejemplo_1>/n/n<texto_string_input_ejemplo_2>/n/n{text_string_two}/n/n</texto_string_input_ejemplo_2>/n/n<dictionary_output_ejemplo_2>/n/n{dictionary_two}/n/n</dictionary_output_ejemplo_2>/n/n<texto_string_input_ejemplo_3>/n/n{text_string_three}/n/n</texto_string_input_ejemplo_3>/n/n<dictionary_output_ejemplo_3>/n/n{dictionary_three}/n/n</dictionary_output_ejemplo_3>"
    # TODO: Creacte three version of system content: system_content_imss, system_content_infonavit, system_content_sat

    text_string_unseen = unseen_text

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_content},
            {
                "role": "user",
                "content": f"Extre la información requerida del sigueinte texto string nuevo: /n/n {text_string_unseen}",
            },
        ],
    )

    completion = completion.choices[0].message.content
    # TODO: json.loads()
    completion = JsonHandler.to_dict(completion)
    return completion
