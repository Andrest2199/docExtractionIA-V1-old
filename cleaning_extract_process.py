# %% Process Data%%
import json
import unicodedata
import re
import os
from unidecode import unidecode
from utils.json_handler import JsonHandler

""" TODO:  
        - Createformat: "from datetime import datetime"
        - Definir main para controlar funciones
        """
def txt_cleaning(texto):
    if "|" not in texto and texto.startswith('"'):
        texto = texto.strip()
        texto = texto.split('"')
        texto = texto[1].replace("\n", "|")
    elif "\n" in texto:
        texto = texto.replace("\n", "|")
    else:
        texto = texto.replace(" ", "|")
    
    # Decodificamos caracteres UTF-8
    patron = re.compile(r'\\u([\d\w]{4})')
    temp_text = patron.sub(lambda x: unidecode(chr(int(x.group(1), 16))), texto)
    # Normalizamos caracteres que se hayan escapado
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", temp_text)
        if unicodedata.category(c) != "Mn"
    )
    # Formateamos UPPERCASE
    texto = texto.upper()
    return texto


def json_cleaning(json_str):
    clear_json = {}
    # Detectamos si es un lista
    if type(json_str) is list:
        json_str = dict(zip(range(len(json_str)), json_str))
        json_str = json.dumps(json_str)

    # Nos quedamos con caracteres alfanumericos, espacios, y simbología de string JSON
    patron = re.compile(r'[^\w\s":{},\.\[\]\/\\]+')
    json_str = patron.sub("", json_str)
    # Decodificamos caracteres UTF-8
    patron = re.compile(r'\\u([\d\w]{4})')
    json_str = patron.sub(lambda x: unidecode(chr(int(x.group(1), 16))), json_str)
    # Limpiamos espacios y formateamos UPPERCASE
    json_str = json_str.strip()
    json_str = json_str.upper()
    # Construimos Diccionario
    decoded_json = JsonHandler.to_dict(json_str)
    # Normalizamos caracteres que se hayan escapado
    normalized_json = {
        (
            key
            if unicodedata.is_normalized("NFKD", str(key))
            else unicodedata.normalize("NFKD", str(key))
        ): (
            value
            if unicodedata.is_normalized("NFKD", str(value))
            else unicodedata.normalize("NFKD", str(value))
        )
        for key,value in decoded_json.items()
    }
    # Formateamos claves [espacios->'_']
    for key, value in normalized_json.items():
        if " " in key:
            normalized_key = key.replace(" ", "_")
            clear_json[normalized_key] = value
        else:
            clear_json[key] = value

    if clear_json == {}:
        # print (f'There are no white space or can\'t replace in keys')
        clear_json = normalized_json

    return clear_json


def json_extraction(json_data=any, type_doc=str)->dict:
    # Limpiamos json de entrada
    try:
        json_data=json_cleaning(json_data)
    except Exception as e:
        raise Exception (f"Error: {e}, fail attempting json_cleaning fuction...")
        
    bool_tipo = False
    # Definimos campos y sus variaciones
    campos_variaciones = {
        "IMSS":{
            "SERIE_Y_FOLIO":
                {"serie":"",
                "folio":"",
                "serie_y_folio":""},
            "POSIBLE_RIESGO_TRABAJO":
                {"riesgo":"",
                "trabajo":"",
                "probable":"",
                "riesgo_trabajo":"",
                "posible_riesgo":"",
                "posible_riesgo_trabajo":"",
                "probable_riesgo_trabajo":""},
            "RAMO_INCAPACIDAD":
                {"seguro":"",
                "ramo":"",
                "ramo_seguro":"",
                "ramo_de_seguro":""},
            "FECHA_A_PARTIR":
                {"partir":"",
                "a_partir":"",
                "a_partir_de":"",
                "inicio":"",
                "incapacidad":"",
                "inicio_incapacidad":""},
            "FECHA_EXPEDIDO":
                {"expedido":"",
                "expedido_el":""},
            "DIAS_INCAPACIDAD":
                {"numero":"",
                "dias":"",
                "autorizados":"",
                "dias_autorizados_letra":"",
                "numero_dias_autorizados":""}
        },
        "INFONAVIT": {#hay dos tipos: altas de credito/suspension
            # {"#Numero de empleado"},#Viene en el nombre del archivo
            "TITULO_DOCUMENTO": #solo para altas de credito
                {"aviso_para_retencion_de_descuentos":"",
                 "retencion_de_descuentos":"",
                 "inicio_tramite":"",
                 "inicio_de_tramite":"",
                 "acuse_de_notificacion_de_inicio_de_tramite":"",
                 "notificacion_de_inicio_de_tramite":""},
            "FECHA_DEL_DOCUMENTO":#extraer mes y año
                {"fecha":"",
                 "fecha_recepcion":"",
                 "fecha_de_recepcion":""},
            "NUMERO_DE_CREDITO":
                {"numero_de_credito":"",
                "numero":"",
                "credito":"",
                "numero_credito":""},
            "CANTIDAD_DE_DESCUENTO":
                {"descuento_mensual":"",
                "porcentaje":"",
                "pesos":"",
                "factor_de_descuento":"",
                "factor_descuento":"",
                "descuento":"",
                "factor_de_cuota_en_vsm":"",
                "cuota_en_vsm":"",
                "factor_cuota_vsm":"",
                "cuota_vsm":"",
                "monto_de_descuento":"",
                "monto_descuento":""},
            "MOTIVO_BAJA": #solo para cuando son suspensiones
                {"aviso_suspension":"",
                "aviso_de_suspension":"",
                "aviso_de_suspension_de_descuentos":"",
                "suspension_de_descuentos":"",
                "suspension_descuentos":""}
        },
        "SAT": {
            "RFC":
                {"rfc":""},
            "CURP":
                {"curp":"",
                 "r[A-Z]{4}[0-9]{6}[H,M][A-Z]{5}[A-Z0-9]{2}":""},
            "NOMBRE":
                {"nombre s":"",
                 "nombre":""},
            "PRIMER_APELLIDO":
                {"primer":"",
                "primer_apellido":""},
            "SEGUNDO_APELLIDO":
                {"segundo":"",
                "segundo_apellido":""},
            "CODIGO_POSTAL":
                {"codigo":"",
                "postal":"",
                "codigo_postal":"",
                "rPOSTAL\s?:?(\d{5})":""}
        },
    }

    if type_doc == "":
        return "You need to defined the type of document..."

    for tipo in campos_variaciones.keys():
        if tipo == type_doc:
            bool_tipo = True
            informacion_extraida = campos_variaciones.get(type_doc)

    if bool_tipo == False:
        return "The type of document does not exist..."

    bool_nested_dict = False
    for valor in json_data.values():
        if isinstance(valor, dict):
            bool_nested_dict = True

    # Buscar coincidencias en el Diccionario/JSON
    for main_key,sub_keys in informacion_extraida.items():
        for sub_key in sub_keys.keys():
            if bool_nested_dict == False:
                if json_data.get(sub_key.upper()):
                    informacion_extraida[main_key][sub_key]=json_data.get(sub_key.upper()).strip() 
                elif sub_key.startswith('r'):
                    patron = sub_key[1:]
                    exp_compilada = re.compile(r'(?:'+patron+')')
                    temp_string = str(json_data)
                    coincidencias = exp_compilada.search(temp_string)
                    if coincidencias != None:
                        informacion_extraida[main_key][sub_key]= coincidencias.group()
                else: 
                    informacion_extraida[main_key][sub_key]=None
                    patron = re.escape(sub_key.upper())
                    exp_compilada = re.compile(patron)
                    for keyJson in json_data.keys():
                        coincidencias = exp_compilada.search(keyJson)
                        if coincidencias != None:
                            informacion_extraida[main_key][sub_key]= json_data.get(keyJson)
                            break
            elif bool_nested_dict == True:
                for clave,nest_clave in json_data.items():
                    if isinstance(nest_clave,dict):
                        if json_data[clave].get(sub_key.upper()):
                            informacion_extraida[main_key][sub_key]=json_data[clave].get(sub_key.upper()).strip()
                            break
                        elif sub_key.startswith('r'):
                            patron = sub_key[1:]
                            exp_compilada = re.compile(r'(?:'+patron+')')
                            temp_string = str(json_data[clave])
                            coincidencias = exp_compilada.search(temp_string)
                            if coincidencias != None:
                                informacion_extraida[main_key][sub_key]= coincidencias.group()
                        else: 
                            informacion_extraida[main_key][sub_key]=None
                            patron = re.escape(sub_key.upper())
                            exp_compilada = re.compile(patron)
                            for keyJson in json_data[clave].keys():
                                coincidencias = exp_compilada.search(keyJson)
                                if coincidencias != None:
                                    informacion_extraida[main_key][sub_key]= json_data[clave].get(keyJson)
                                    flag=True
                                    break
                    else:
                        if json_data.get(sub_key.upper()):
                            informacion_extraida[main_key][sub_key]=json_data.get(sub_key.upper()).strip() 
                            break
                        elif sub_key.startswith('r'):
                            patron = sub_key[1:]
                            exp_compilada = re.compile(r'(?:'+patron+')')
                            temp_string = str(json_data)
                            coincidencias = exp_compilada.search(temp_string)
                            if coincidencias != None:
                                informacion_extraida[main_key][sub_key]= coincidencias.group()
                        else: 
                            informacion_extraida[main_key][sub_key]=None
                            patron = re.escape(sub_key.upper())
                            exp_compilada = re.compile(patron)
                            for keyJson in json_data.keys():
                                coincidencias = exp_compilada.search(keyJson)
                                if coincidencias != None:
                                    informacion_extraida[main_key][sub_key]=json_data.get(keyJson)
                                    break


    return informacion_extraida


def txt_extraction(txt_str=str,type_doc=str)->dict:
    # Limpiamos texto de entrada
    try:
        texto = txt_cleaning(txt_str)
    except Exception as e:
        raise Exception (f"Error: {e}, fail attempting json_cleaning fuction...")
        
    bool_tipo = False
    arr_coincidencias = {}
    # Definimos campos y patrones
    patrones_regulares = {
        "IMSS":{
            "SERIE_FOLIO": [
                "SERIE\s?\|?Y\s?\|?FOLIO\s?\|?(.*?)\|",
                "SERIE\s?\|?FOLIO\s?\|?(.*?)\|",
                "SERIE\s?\|?(.*?)\|"],
            "TIPO_INCAPACIDAD": [
                "TIPO\s?\|?INCAPACIDAD\s?\|?(.*?)\|",
                "INCAPACIDAD\s?\|?(.*?)\|"],
            "RAMO_SEGURO": [
                "RAMO\s?\|?DE\s?\|?SEGURO\s?\|?(.*?)\|?(.*?)\|",
                "SEGURO\s?\|?(.*?)\s?\|?(.*?)\|"],
            "FECHA_APARTIR": [
                "PARTIR\s?\|?DEL\s?\|?(.*?)\|"],
            "FECHA_EXPEDIDO": [
                "EXPEDIDO\s?\|?EL\s?\|?(.*?)\|"],
            "PROBABLE_RIESGO_TRABAJO": [
                "RIESGO\s?\|?TRABAJO\s?\|?(.*?)\|",
                "RIESGO\s?\|?DE\s?\|?TRABAJO\s?\|?(.*?)\|"],
            "DIAS_AUTORIZADOS": [
                "DIAS\s?\|?AUTORIZADOS\s?\|?\(\|?LETRA\|?\)\s?\|?(.*?)\|",
                "DIAS\s?\|?AUTORIZADOS\s?\|?(.*?)\|"]
        },
        "INFONAVIT":{
            "TITULO_DOCUMENTO": [
                "AVISO\s?\|?PARA\s?\|?RETENCION\s?\|?DE\s?\|?DESCUENTOS",
                "RETENCION\s?\|?DE\s?\|?DESCUENTOS",
                "INICIO\s?\|?TRAMITE",
                "INICIO\s?\|?DE\s?\|?TRAMITE",
                "ACUSE\s?\|?DE\s?\|?NOTIFICACION\s?\|?DE\s?\|?INICIO\s?\|?DE\s?\|?TRAMITE",
                "NOTIFICACION\s?\|?DE\s?\|?INICIO\s?\|?DE\s?\|?TRAMITE",
            ],
            "FECHA": [
                "FECHA\s?\|?:?\s?\|?(\d{2}\/\d{2}\/\d{4})\|?",
                "\s?\|?(\d{2}\/\d{2}\/\d{4})\s?\|?"
            ],
            "NUMERO_DE_CREDITO": [
                "NUMERO\s?\|?DE\s?\|?CREDITO\s?\|?:?\s?\|?(\d)+\|?",
                "CREDITO\s?\|?:?\s?\|?(\d)+\|?",
                "\|(\d{10})\|",
                "\s(\d{10})\s",
                "CREDITO\s?\|?:?\s?\|?(\*)+(\d)+\|?",
            ],
            "CANTIDAD_DE_DESCUENTO": [
                "MONTO\s?\|?DE\s?\|?DESCUENTO\s?\|?:?\s?\|?(.*?(\d)+)\|?",
                "FACTOR\s?\|?DE\s?\|?CUOTA\s?\|?EN\s?\|?VSM\s?\|?:?\s?\|?(\d)+\.(\d)+\|?",
                "CUOTA\s?\|?EN\s?\|?VSM\s?\|?:?\s?\|?(\d)+\.(\d)+\|?",
                "FACTOR\s?\|?CUOTA\s?\|?VSM\s?\|?:?\s?\|?(\d)+\.(\d)+\|?",
                "CUOTA\s?\|?VSM\s?\|?:?\s?\|?(\d)+\.(\d)+\|?",
                "PORCENTAJE\s?\|?:?\s?\|?(.*?)\|",
                "PESOS\s?\|?:?\s?\|?(.*?)\|",
                "FACTOR\s?\|?DE\s?\|?DESCUENTO\s?\|?:?\s?\|?(.*?)\|",
                "FACTOR\s?\|?DESCUENTO\s?\|?:?\s?\|?(.*?)\|",
                "DESCUENTO\s?\|?:?\s?\|?(.*?)\|"
            ],
            "MOTIVO_BAJA": [
                "AVISO\s?\|?DE\s?\|?SUSPENSION\s?\|?DE\s?\|?DESCUENTOS",
                "SUSPENSION\s?\|?DE\s?\|?DESCUENTOS",
                "AVISO\s?\|?DE\s?\|?SUSPENSION",
                "AVISO\s?\|?SUSPENSION",
                "SUSPENSION\s?\|?DESCUENTOS",
                "SUSPENSION"
            ]
        },
        "SAT":{
            "RFC":
                ["RFC\|?\s?:?\s?\|?([A-Z]{3,4}[0-9]{6}[A-Z0-9]{3})\|?",
                 "RFC\|?\s?:?\|?(.*?)\|",
                 "\s?\|?([A-Z]{3,4}[0-9]{6}[A-Z0-9]{3})\s?\|?"],
            "CURP":
                ["CURP\|?\s?:?\s?\|?([A-Z]{4}[0-9]{6}[H,M][A-Z]{5}[A-Z0-9]{2})\|?",
                 "CURP\|?\s?:?\|?(.*?)\|",
                 "\s?\|?([A-Z]{4}[0-9]{6}[H,M][A-Z]{5}[A-Z0-9]{2})\s?\|?"],
            "NOMBRE":
                ["NOMBRE\|?\(S\)?:?\|?(.*?)\|",
                 "NOMBRE\|?\(S\)?:?\s?\|?([A-Z']+(\s[A-Z']+)*)\|?",
                 "NOMBRE\|?\(S\)?:?\s?\|?([A-Za-z']+(\s[A-Za-z']+)*)\|?"],
            "PRIMER_APELLIDO":
                ["PRIMER\|?\s?:?\s?\|?([A-Z]+)?\:?\s?\|?([A-Z']+(\s[A-Z']+)*)\|?",
                 "PRIMER\s?\|?APELLIDO\|?\s?:?\s?\|?([A-Z']+(\s[A-Z']+)*)\|?"],
            "SEGUNDO_APELLIDO":
                ["SEGUNDO\|?\s?:?\s?\|?([A-Z]+)?\:?\s?\|?([A-Z']+(\s[A-Z']+)*)\|?",
                "SEGUNDO\s?\|?APELLIDO\|?\s?:?\s?\|?([A-Z']+(\s[A-Z']+)*)\|?"],
            "CODIGO_POSTAL":
                ["CODIGO\s?([A-Z]+)?\|?\s?:?\|?\s?(\d{5})\|?",
                 "POSTAL\|?\s?:?\s?\|?(\d{5})\|?",
                 "CODIGO\|?\s?POSTAL\|?\s?:?\|?\s?(\d{5})\|?",
                 "CODIGO\|?\s?POSTAL\|?\s?:?\|?\s?(.*?)\|",
                 "\s?\|?(\d{5})\s?\|?"]
        }
    }
    
    if type_doc == "":
        return "You need to defined the type of document..."

    for tipo in patrones_regulares.keys():
        if tipo == type_doc:
            bool_tipo = True
            patrones = patrones_regulares.get(type_doc)

    if bool_tipo == False:
        return "The type of document does not exist..."
    
    # Buscar coincidencias en el texto
    for key, pat in patrones.items():
        arr_coincidencias[key] = {}
        if type(pat) is str:
            patron = re.compile(r"(?:" + pat + ")")
            coincidencias = patron.search(texto)
            if coincidencias:
                arr_coincidencias[key] = coincidencias.group()
            else:
                arr_coincidencias[key] = None
        elif type(pat) is list:
            i = 0
            for pat2 in pat:
                i += 1
                patron = re.compile(r"(?:" + pat2 + ")")
                coincidencias = patron.search(texto)
                if coincidencias:
                    new_value = {str(i):coincidencias.group()}
                    arr_coincidencias[key].update(new_value)
                else:
                    new_value = {str(i):None}
                    arr_coincidencias[key].update(new_value)

    return arr_coincidencias



# #%% TEST TXT SIN DELIMITADOR '|'-----------------------------
# folder_base_path = os.getcwd()+'/3_text_extracted'
# file_path_input = os.path.join(folder_base_path, '0_procesed_text_PT.txt')
# with  open(file_path_input) as archivo:
#     json_str = archivo.read()

# info_extraida=txt_extraction(json_str)
# print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
# #%% TEST TXT CON DELIMITADOR '|'-----------------------------
# folder_base_path = os.getcwd()+'/3_text_extracted'
# file_path_input = os.path.join(folder_base_path, '695844 MACIAS LARA JORGE ARMANDO VZ 948810 ok.jpg_procesed.jpeg_AWS_extract.txt')
# with  open(file_path_input) as archivo:
#     json_str = archivo.read()

# info_extraida=txt_extraction(json_str)
# print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
# #%% TEST JSON------------------------------------------------
# folder_base_path = os.getcwd()+'/3_text_extracted'
# file_path_input = os.path.join(folder_base_path, '734031 GONZALEZ FRANCO BRISEIDA VL 865277 OK_procesed_0_1_X2.jpeg_AWS_analyzed.txt')

# with  open(file_path_input) as archivo:
#     json_str = archivo.read()
# #Limpieza del JSON
# data_clean=json_cleaning(json_str)
# #Extracción de información
# informacion_extraida = json_extraction(data_clean,'IMSS')
# print("\nInformación extraída:")
# print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2))

#%% TEST FINAL
folder_base_path = os.getcwd()+'/3_text_extracted'
output_folder_path = os.getcwd()+'/4_results'
"""INFONAVIT"""
for i in range(0,5):
    file_path_input = os.path.join(folder_base_path, str(i)+'.txt')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    info_extraida=txt_extraction(json_str,'INFONAVIT')
    # print(f"\nInformación extraída de {i}.txt:")
    # print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
    json_content=json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_INFONAVIT.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)

for i in range(5,7):
    file_path_input = os.path.join(folder_base_path, str(i)+'.json')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    informacion_extraida = json_extraction(json_str,'INFONAVIT')
    # print(f"\nInformación extraída de {i}.json:")
    # print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2))
    json_content=json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_INFONAVIT.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)
    
"""SAT"""
for i in range(7,11):
    file_path_input = os.path.join(folder_base_path, str(i)+'.txt')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    info_extraida=txt_extraction(json_str,'SAT')
    # print(f"\nInformación extraída de {i}.txt:")
    # print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
    json_content=json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_SAT.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)

for i in range(11,13):
    file_path_input = os.path.join(folder_base_path, str(i)+'.json')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    informacion_extraida = json_extraction(json_str,'SAT')
    # print(f"\nInformación extraída de {i}.json:")
    # print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True))
    json_content=json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_SAT.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)


"""IMSS"""
for i in range(13,25):
    file_path_input = os.path.join(folder_base_path, str(i)+'.txt')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    info_extraida=txt_extraction(json_str,'IMSS')
    # print(f"\nInformación extraída de {i}.txt:")
    # print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
    json_content=json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_IMSS.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)

for i in range(25,33):
    file_path_input = os.path.join(folder_base_path, str(i)+'.json')
    with  open(file_path_input) as archivo:
        json_str = archivo.read()
    #Extracción de información
    informacion_extraida = json_extraction(json_str,'IMSS')
    # print(f"\nInformación extraída de {i}.json:")
    # print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True))
    json_content=json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True)
    new_file_name = 'result_'+str(i)+ "_IMSS.json"
    file_path_output = os.path.join(output_folder_path, new_file_name)
    with open(file_path_output, "w") as file:
        file.write(json_content)


# %%
