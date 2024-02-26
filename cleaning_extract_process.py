# %% pre process data data%%
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
    clear_json = None

    # Detectamos si es un txt
    if type(json_str) is list:
        json_str = dict(zip(range(len(json_str)), json_str))
        json_str = json.dumps(json_str)

    # Nos quedamos con caracteres alfanumericos, espacios, y simbología de string JSON
    patron = re.compile(r'[^\w\s":{},\[\]\/]+')
    json_str = patron.sub("", json_str)
    json_str = json_str.strip()
    json_str = json_str.upper()
    decoded_json = JsonHandler.to_dict(json_str)
    # decoded_json = json.loads(json_str)

    for key in decoded_json.keys():
        if key.find(" ") > 0:
            key_value = key.replace(" ", "_")
            clear_json = {
                clave if clave != key else key_value: valor
                for clave, valor in decoded_json.items()
            }

    if clear_json == None:
        clear_json = decoded_json

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
        for key, value in clear_json.items()
    }

    return normalized_json


def data_extraction(json_data, type_doc):
    """CAMPOS PRINCIPALES / OPERACIONES
        INCAPACIDADES:
        extras,folio,posible_riesgo,fecha_desde,
        dias_incapacidad,rama_incapacidad
        tipo_incapacidad : #EG,MA,AT se obtiene de rama_incapacidad
        INFONAVIT:
        numero_credito,
        fecha,
        aviso [titulo de doc]
    CAMPOS PRINCIPALES / CODIGOS POSTALES
        rfc,curp,nombre,primer_apellido,
        segundo_apellido,codigo_postal
    """
    contador_tipo = 0
    campos_variaciones = {
        # TODO: cambiar a IMSS, INFONAVTI, SAT
        "incapacidades": [  # Extras
            "institucion",
            "nombre",
            "institucion",
            "curp",
            # Serie
            "serie",
            "folio",
            # Posible riesgo
            "riesgo",
            "trabajo",
            "probable",
            "probable_riesgo_trabajo",
            # Rama incapacidad
            "seguro",
            "ramo",
            "ramo_seguro",
            "ramo_de_seguro",
            # Fecha desde
            "partir",
            "a_partir",
            "a_partir_de",
            "inicio",
            "incapacidad",
            "inicio_incapacidad",
            # Fecha desde en otro campo
            "expedido",
            "expedido_el",
            # Dias Incapacidad
            "numero",
            "dias",
            "autorizados",
            "dias_autorizados_letra",
            "numero_dias_autorizados",
            "direccion",
        ],
        "infonavit": [
            "numero",
            "credito",
            "numero_credito",
            "fecha",
            "aviso",
            "suspension",
            "aviso_suspension",
        ],
        "codigos_postales": [
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
        return "Debe definir un tipo de documento."

    for tipo in campos_variaciones.keys():
        if tipo == type_doc:
            contador_tipo += 1
            variaciones = campos_variaciones.get(type_doc)

    if contador_tipo == 0:
        return "No existe el tipo de documento"

    for i in range(len(variaciones)):
        variaciones[i] = variaciones[i].upper()
    informacion_extraida = {
        campo.strip(): (
            json_data.get(campo).strip() if json_data.get(campo.strip()) else "NA"
        )
        for campo in variaciones
    }

    for key, value in informacion_extraida.items():
        if value == "NA":
            patron = re.escape(key)
            exp_compilada = re.compile(patron)
            for keyJson in json_data.keys():
                coincidencias = exp_compilada.search(keyJson)
                if coincidencias != None:
                    informacion_extraida[key] = json_data.get(keyJson)

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
    else:
        texto = texto.replace("\n", "|")
    # Formatear string
    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    texto = texto.upper()
    # Definir el patrón regex
    # patron_regex = re.compile(r"(?:TIPO\|INCAPACIDAD\|(.*?)\|).*?(?:RAMO\|DE\|SEGURO\|(.*?)\|(.*?)\|).*?(?:RIESGO\|TRABAJO\|(.*?)\|).*?(?:DIAS\|AUTORIZADOS\|\(\|LETRA\|\)\|(.*?)\|).*?(?:SERIE\|Y\|FOLIO\|(.*?)\|).*?(?:PARTIR\|DEL\|(.*?)\|).*?(?:EXPEDIDO\|EL\|(.*?)\|)")
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
file_path_input = os.path.join(folder_base_path, '1_procesed_0_0_Im0_HW.txt')
with  open(file_path_input) as archivo:
    json_str = archivo.read()

info_extraida=regex_extraction(json_str)
print(json.dumps(info_extraida,ensure_ascii=False,indent=2,sort_keys=True))
#%% TEST JSON------------------------------------------------
folder_base_path = os.getcwd()+'/3_text_extracted'
file_path_input = os.path.join(folder_base_path, '01.json')
with  open(file_path_input) as archivo:
    json_str = archivo.read()

#Limpieza del JSON
data_clean=data_cleaning(json_str)
#Extracción de información
informacion_extraida = data_extraction(data_clean,'operaciones','incapacidades')
print("\nInformación extraída:")
print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True))


# %% TEST LIST%%
json_str = ['test','test2']
"""
