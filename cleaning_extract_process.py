# %% pre process data%%
import json
import unicodedata
import re
import os
from utils.json_handler import JsonHandler

""" TODO:  
        - createformat. "from datetime import datetime"
        - Juntar funciones o definir union data_cleaning,data_extraction,regex_extraction
        """

def data_cleaning(json_str):
    clear_json = {}
    # Detectamos si es un lista
    if type(json_str) is list:
        json_str = dict(zip(range(len(json_str)), json_str))
        json_str = json.dumps(json_str)

    # Nos quedamos con caracteres alfanumericos, espacios, y simbología de string JSON
    patron = re.compile(r'[^\w\s":{},\[\]\/\\]+')
    json_str = patron.sub("", json_str)
    patron = re.compile(r'\\u([\d\w]{4})')
    json_str = patron.sub(lambda x: chr(int(x.group(1), 16)), json_str)
    json_str = json_str.strip()
    json_str = json_str.upper()
    decoded_json = JsonHandler.to_dict(json_str) 

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
        for key, value in decoded_json.items()
    }

    for key, value in normalized_json.items():
        if " " in key:
            normalized_key = key.replace(" ", "_")
            clear_json[normalized_key] = value
        else:
            clear_json[key] = value

    if clear_json == {}:
        print (f'There are no white space or Can\'t replace in keys')
        clear_json = normalized_json

    return clear_json


def data_extraction(json_data, type_doc):
    """CAMPOS PRINCIPALES
    IMSS:
            extras,folio,posible_riesgo,fecha_desde,
            dias_incapacidad,rama_incapacidad
            tipo_incapacidad : #EG,MA,AT se obtiene de rama_incapacidad
    INFONAVIT:
            numero_credito,
            fecha,
            aviso [titulo de doc]
    SAT
        rfc,curp,nombre,primer_apellido,
        segundo_apellido,codigo_postal
    """
    contador_tipo = 0
    campos_variaciones = {
        "IMSS":[
            # {"#Extras":
            #     {"institucion":"",
            #     "nombre":"",
            #     "institucion":"",
            #     "curp":""}},
            {"#Serie y Folio":
                {"serie":"",
                "folio":"",
                "serie_y_folio":""}},
            {"#Posible Riesgo":
                {"riesgo":"",
                "trabajo":"",
                "probable":"",
                "riesgo_trabajo":"",
                "posible_riesgo":"",
                "posible_riesgo_trabajo":"",
                "probable_riesgo_trabajo":""}},
            {"#Rama Incapacidad":
                {"seguro":"",
                "ramo":"",
                "ramo_seguro":"",
                "ramo_de_seguro":""}},
            {"#Fecha desde":
                {"partir":"",
                "a_partir":"",
                "a_partir_de":"",
                "inicio":"",
                "incapacidad":"",
                "inicio_incapacidad":""}},
            {"#Fecha de Expedido":
                {"expedido":"",
                "expedido_el":""}},
            {"#Dias Incapacidad":
                {"numero":"",
                "dias":"",
                "autorizados":"",
                "dias_autorizados_letra":"",
                "numero_dias_autorizados":""}}
        ],
        "INFONAVTI": [
            "numero",
            "credito",
            "numero_credito",
            "fecha",
            "aviso",
            "suspension",
            "aviso_suspension",
        ],
        "SAT": [
            "rfc",
            "curp",
            "nombre",
            "primer",
            "primer_apellido",
            "segundo",
            "segundo_apellido",
            "codigo",
            "postal",
            "codigo_postal",
        ],
    }
    if type_doc == "":
        return "You need to defined the type of document."

    for tipo in campos_variaciones.keys():
        if tipo == type_doc:
            contador_tipo += 1
            informacion_extraida = campos_variaciones.get(type_doc)

    if contador_tipo == 0:
        return "There type of document doesn not exist."

    for pos in range(len(informacion_extraida)):
        for main_key,sub_keys in informacion_extraida[pos].items():
            for sub_key in sub_keys.keys():
                if json_data.get(sub_key.upper()):
                    informacion_extraida[pos][main_key][sub_key]=json_data.get(sub_key.upper()).strip() 
                else:
                    informacion_extraida[pos][main_key][sub_key]="NA"
                    patron = re.escape(sub_key.upper())
                    exp_compilada = re.compile(patron)
                    for keyJson in json_data.keys():
                        coincidencias = exp_compilada.search(keyJson)
                        if coincidencias != None:
                            informacion_extraida[pos][main_key][sub_key]= json_data.get(keyJson)
                            break

    return informacion_extraida


def regex_extraction(texto):
    # TODO: ADD trycatch for logging
    print("texto a procesar", texto)
    # Detectar si hay '|'
    boolBarra = True
    if "|" not in texto and '"' in texto:
        boolBarra = False
        texto = texto.strip()
        texto = texto.split('"')
        texto = texto[1].replace("\n", "|")
    elif "\n" in texto:
        texto = texto.replace("\n", "|")
    else:
        texto = texto.replace(" ", "|")
    
    # Formatear string
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    texto = texto.upper()
    print (f'texto:{texto}')
    # Definir el patrón regex
    arr_coincidencias = {}
    patrones_regulares = {
        "SERIE_FOLIO": "SERIE\|Y\|FOLIO\|(.*?)\|",
        "TIPO_INCAPACIDAD": "TIPO\|INCAPACIDAD\|(.*?)\|",
        # "INCAPACIDAD\|(.*?)\|"],
        "RAMO_SEGURO": "RAMO\|DE\|SEGURO\|(.*?)\|(.*?)\|",
        # "SEGURO\|(.*?)\|(.*?)\|"],
        "FECHA_APARTIR": "PARTIR\|DEL\|(.*?)\|",
        "FECHA_EXPEDIDO": "EXPEDIDO\|EL\|(.*?)\|",
        "PROBABLE_RIESGO_TRABAJO": "RIESGO\|TRABAJO\|(.*?)\|",
        "DIAS_AUTORIZADOS": "DIAS\|AUTORIZADOS\|\(\|LETRA\|\)\|(.*?)\|",
    }
    if boolBarra == False:
        patrones_regulares = {
            "SERIE_FOLIO": "SERIE Y FOLIO(.*?)\|",
            "TIPO_INCAPACIDAD": "TIPO INCAPACIDAD\|?(.*?)\|",
            "RAMO_SEGURO": "RAMO DE SEGURO\|?(.*?)\|",
            "FECHA_APARTIR": "PARTIR DEL\|?(.*?)\|",
            "FECHA_EXPEDIDO": "EXPEDIDO EL\|?(.*?)\|",
            "PROBABLE_RIESGO_TRABAJO": "RIESGO\|TRABAJO\|?(.*?)\|",
            "DIAS_AUTORIZADOS": "DIAS AUTORIZADOS\(LETRA\)\|?(.*?)\|",
        }
    # Buscar coincidencias en el texto
    for key, pat in patrones_regulares.items():
        if type(pat) is str:
            patron = re.compile(r"(?:" + pat + ")")
            coincidencias = patron.search(texto)
            if coincidencias:
                if len(coincidencias.groups()) > 1:
                    value = ""
                    for data in coincidencias.groups():
                        value += data + " "
                    arr_coincidencias[key] = value.strip()
                else:
                    arr_coincidencias[key] = coincidencias.group(1)
            else:
                arr_coincidencias[key] = "NA"
        elif type(pat) is list:
            i = 0
            for pat2 in pat:
                i += 1
                patron = re.compile(r"(?:" + pat2 + ")")
                coincidencias = patron.search(texto)
                if coincidencias:
                    if len(coincidencias.groups()) > 1:
                        value = ""
                        for data in coincidencias.groups():
                            value += data + " "
                        arr_coincidencias[key + "_" + str(i)] = value.strip()
                    else:
                        arr_coincidencias[key + "_" + str(i)] = coincidencias.group(1)
                else:
                    arr_coincidencias[key + "_" + str(i)] = "NA"

    return arr_coincidencias


"""
#%% TEST TXT SIN DELIMITADOR '|'-----------------------------
folder_base_path = os.getcwd()+'/3_text_extracted'
file_path_input = os.path.join(folder_base_path, '0_procesed_text_PT.txt')
with  open(file_path_input) as archivo:
    json_str = archivo.read()

info_extraida=regex_extraction(json_str)
print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
#%% TEST TXT CON DELIMITADOR '|'-----------------------------
folder_base_path = os.getcwd()+'/3_text_extracted'
file_path_input = os.path.join(folder_base_path, '695844 MACIAS LARA JORGE ARMANDO VZ 948810 ok.jpg_procesed.jpeg_AWS_extract.txt')
with  open(file_path_input) as archivo:
    json_str = archivo.read()

info_extraida=regex_extraction(json_str)
print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
#%% TEST JSON------------------------------------------------
folder_base_path = os.getcwd()+'/3_text_extracted'
file_path_input = os.path.join(folder_base_path, '734031 GONZALEZ FRANCO BRISEIDA VL 865277 OK_procesed_0_1_X2.jpeg_AWS_analyzed.txt')

with  open(file_path_input) as archivo:
    json_str = archivo.read()

#Limpieza del JSON
data_clean=data_cleaning(json_str)
#Extracción de información
informacion_extraida = data_extraction(data_clean,'IMSS')
print("\nInformación extraída:")
print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2))


# %% TEST LIST%%
json_str = ['test','test2']
"""
