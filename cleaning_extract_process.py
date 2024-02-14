# %% pre process data data%%
import json
import unicodedata
import re
import os

""" TODO:  - lowercase y espacios a '_'
           - createformat
        """


def limpiar_json(json_str):
    # Nos quedamos con caracteres alfanumericos, espacios, y simbología de string JSON
    patron = re.compile(r'[^\w\s":{},\[\]\\]+')

    json_str = patron.sub("", json_str)
    json_str = json_str.strip()
    json_str = json_str.lower()
    print(json_str)
    decoded_json = json.loads(json_str)
    print(decoded_json)
    for key, value in list(decoded_json.items()):
        if key.find(" ") > 0:
            keyValue = key.replace(" ", "_")
            decoded_json[keyValue] = decoded_json[key]
            del decoded_json[key]

    normalized_json = {
        (
            key.replace(" ", "_")
            if unicodedata.is_normalized("NFKD", str(key))
            else unicodedata.normalized("NFKD", str(key))
        ): (
            value
            if unicodedata.is_normalized("NFKD", str(value))
            else unicodedata.normalize("NFKD", str(value))
        )
        for key, value in decoded_json.items()
    }

    return normalized_json


def extraer_informacion(json_data):
    """
    #CAMPOS PRINCIPALES
        #"extras"
        #"folio"
        #"posible_riesgo"
        #"fecha_desde"
        #"dias_incapacidad"
        #"rama_incapacidad"
        #"tipo_incapacidad" : #EG,MA,AT se obtiene de rama_incapacidad
    """
    campos_variaciones = [
        # Extras
        "nombre_asegurado",
        "institucion prueba",
        "curp",
        "serie_folio",
        # Posible riesgo
        "probable_riesgo_trabajo",
        # Rama incapacidad
        "ramo_seguro",
        "ramo_de_seguro",
        "Ramo de Seguro",
        # Fecha desde
        "a_partir_de",
        "A partir del",
        "inicio_incapacidad",
        # Fecha desde en otro campo
        "expedido_el",
        "Expedido el",
        # Dias Incapacidad
        "numero",
        "dias_autorizados_letra",
        "numero_dias_autorizados",
        "Dias Autorizados",
        "direccion",
        # Agregar más campos según sea necesario
    ]
    informacion_extraida = {
        campo.strip(): (
            json_data.get(campo, "") if json_data.get(campo) else ":No se encontro"
        )
        for campo in campos_variaciones
    }

    return informacion_extraida


# %% Ejemplo de uso prueba%%
json_str = """
{
    "institucion": "INSTITUTO MEXICANO DEL SEGURO SOCIAL",
    "institucion prueba": "INSTITUTO MEXICANO DEL SEGURO SOCIAL",
    "direccion": "DIRECCI\u00d3N DE PRESTACIONES M\u00c9DICAS",
    "documento": "CERTIFICADO DE INCAPACIDAD TEMPORAL PARA EL TRABAJO",
    "nss": "9000-84-1206",
    "agregado_medico": "1M19840R",
    "nombre_asegurado": "ISIDRO $RAMOS CRUZ",
    "curp": "RACI830115HCMRS00",
    "sexo": "MASCULINO",
    "delegacion": "OAXACA",
    "unidad": {
        "numero": "1",
        "clave_presupuestal": "21012252110"
    },
    "consultorio": "5",
    "turno": "MATUTINO",
    "documento_identificacion_asegurado": "CREDENCIAL PARA VOTAR",
    "numero_identificacion": "I270015670006",
    "serie_folio": "WG667076",
    "unidad_medica_expedidora": "1",
    "nivel_atencion": "1",
    "delegacion_adscripcion": "Oaxaca",
    "tipo_incapacidad": "INICIAL",
    "dias_autorizados": "uno",
    "forma_seguro_enfermedad_general": "NO",
    "probable_riesgo_trabajo": "NO",
    "dias_acumulados": "0",
    "particion": {
        "expedidora": "Oaxaca",
        "serie": "WG667076"
    },
    "patron": {
        "nombre": "LEVI STRAUSS DE MEXICO",
        "puesto_trabajo": "Demostradores y promotores"
    },
    "numero": "1",
    "a_partir_de": "16/12/2023",
    "expedido_el": "16/12/2023",
    "control_maternidad": {
        "no": "NA"
    },
    "nombre_firma_medico": "JAVIER ANTONIO L\u00d3PEZ AQUINO",
    "matricula": "9921974-6",
    "nombre_firma_medico_autoriza": "NO APLICA",
    "matricula_autoriza": "NO APLICA",
    "nota": "El asegurado a quien se entreg\u00f3 copia de este documento se encuentra incapacitado para trabajar a partir de la fecha y durante el periodo que se indica en este estudio.",
    "informacion_adicional": "CONOCES EL SERVICIO DE CONSULTA DE INCAPACIDADES EN LINEA? Ingresa al escritorio virtual y podr\u00e1s revisar el historico de las incapacidades de los trabajadores de tu empresa. Si cuentas con Convenio de pago indirecto y reembolso de subsidios, tambi\u00e9n puedes descargar tus facturas de pago."
}
"""


# %% Limpieza del JSON%%
def data_retrieval(json_file, output_folder):
    with open(json_file, "r") as file:
        data = file.read()
    cleaned_data = limpiar_json(data)
    extracted_data = extraer_informacion(cleaned_data)
    # Extract the file name from the json_file path
    file_name = os.path.basename(json_file)

    with open(os.path.join(output_folder, file_name), "w") as file:
        file.write(
            json.dumps(extracted_data, ensure_ascii=False, indent=2, sort_keys=True)
        )


# json_limpiado = limpiar_json(json_str)

# # %%Extracción de información%%
# informacion_extraida = extraer_informacion(json_limpiado)

# # print("JSON limpiado y con acentos convertidos:")
# # print(json.dumps(json_limpiado,ensure_ascii=False,indent=2,sort_keys=True))

# print("\nInformación extraída:")
# print(informacion_extraida)
# print(json.dumps(informacion_extraida, ensure_ascii=False, indent=2, sort_keys=True))
# %%
