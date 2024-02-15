# %% pre process data data%%
import json
import unicodedata
import re
import os

""" TODO:  
        - createformat. "from datetime import datetime"
        - guardar en un diccionario aparte las coincidencias encontradas 
            y generar un segundo filtrado."""

def limpiar_json(json_str):
    #Detectamos si es un txt
    if type(json_str) is list:        
        json_str = dict(zip(range(len(json_str)), json_str))
        json_str = json.dumps(json_str)
    #Nos quedamos con caracteres alfanumericos, espacios, y simbología de string JSON
    patron = re.compile(r'[^\w\s":{},]+')
    json_str = patron.sub('', json_str)
    json_str=json_str.strip()
    json_str = json_str.upper()
    decoded_json = json.loads(json_str)
    clear_json = None

    for key in decoded_json.keys():
        if key.find(" ") > 0:
            keyValue=key.replace(" ","_")
            clear_json={clave if clave != key else keyValue:valor for clave,valor in decoded_json.items()}
    
    if clear_json == None:
        clear_json = decoded_json
    
    normalized_json = {key if unicodedata.is_normalized('NFKD',str(key)) else unicodedata.normalized('NFKD', str(key)): 
                    value if unicodedata.is_normalized('NFKD', str(value)) else unicodedata.normalize('NFKD', str(value))
                        for key,value in clear_json.items()}

    return normalized_json

def extraer_informacion(json_data,type_doc,subtype_doc=''):
    """ CAMPOS PRINCIPALES / OPERACIONES
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
    contadorTipo = 0
    contadorSubTipo = 0
    campos_variaciones = {
        "operaciones":{
            "incapacidades":
                [#Extras
                "institucion",
                "nombre_asegurado",
                "institucion_prueba",
                "curp",
                "serie_folio",
                #Posible riesgo
                "probable_riesgo_trabajo",
                #Rama incapacidad
                "ramo_seguro",
                "ramo_de_seguro",
                "Ramo de Seguro",
                #Fecha desde
                "partir",
                "a_partir_de",
                "A partir del",
                "inicio_incapacidad",
                #Fecha desde en otro campo
                "expedido_el",
                "Expedido el",
                #Dias Incapacidad
                "numero",
                "dias_autorizados_letra",
                "numero_dias_autorizados",
                "Dias Autorizados",
                "direccion"],
            "infonavit":
                ["numero_credito",
                 "fecha",
                 "aviso_suspension",
                 ]},
        "codigos_postales":[
            "rfc",
            "curp",
            "nombre",
            "primer_apellido",
            "segundo_apellido",
            "codigo_postal"
        ]
    }
    if type_doc == "operaciones" and subtype_doc =="":
        return "Debe definir un subtipo de documento"
    
    if type_doc != "" and subtype_doc == "":
        for tipo in campos_variaciones.keys():
            if tipo == type_doc:
                contadorTipo += 1
                variaciones=campos_variaciones.get(type_doc)
    elif type_doc != "" and subtype_doc != "":
        for tipo,subtipo in campos_variaciones.items():
            if tipo == type_doc:
                contadorTipo += 1
                variaciones = campos_variaciones.get(type_doc)
        for subtipo in variaciones.keys():
            if subtipo == subtype_doc:
                contadorSubTipo += 1
                variacionesFinal = variaciones.get(subtype_doc)
        variaciones = variacionesFinal    
    else:
        return 'El tipo de documento viene vacio'
    
    if contadorTipo == 0:
        return 'No existe el tipo de documento'
    if contadorSubTipo == 0:
        return 'El subtipo de documento viene vacio o no existe'
    for i in range(len(variaciones)):
        variaciones[i] = variaciones[i].upper()
    informacion_extraida = {campo.strip():json_data.get(campo).strip() if json_data.get(campo.strip()) else "No se encontro" for campo in variaciones}
    
    for key,value in informacion_extraida.items():
        if value == "No se encontro":
            # print ("key no encontrado: "+key)
            patron = re.escape(key)
            # print ("patron: "+patron)
            expRegCompilada = re.compile(patron)
            # print ("patron compilado: "+str(expRegCompilada))
            for keyJson in json_data.keys():
                # print("keyJSON: "+keyJson)
                coincidencias = expRegCompilada.search(keyJson)
                if coincidencias != None:
                    informacion_extraida[key]= json_data.get(keyJson)

    return informacion_extraida
# %% Ejemplo de uso prueba%%
json_str = '''
{
    "institucion": "INSTITUTO MEXICANO DEL SEGURO SOCIAL",
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
'''

# %% str list%%
json_str = ['hola','test']

# %% Limpieza del JSON%%
json_limpiado = limpiar_json(json_str)

# %%Extracción de información%%
informacion_extraida = extraer_informacion(json_limpiado,'operaciones','incapacidades')
print("\nInformación extraída:")
print(json.dumps(informacion_extraida,ensure_ascii=False,indent=2,sort_keys=True))
# %%
