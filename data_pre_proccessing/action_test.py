#Ejemplo de uso
# %% Imports%%
import json
from cleaning_extract_process import ProcessingJsonData as functionData

# %% ejecucion prueba%%
json_str = '''
{
    "institucion": "INSTITUTO MEXICANO DEL SEGURO SOCIAL",
    "direccion": "DIRECCI\u00d3N DE PRESTACIONES M\u00c9DICAS",
    "documento": "CERTIFICADO DE INCAPACIDAD TEMPORAL PARA EL TRABAJO",
    "nss": "9000-84-1206",
    "agregado_medico": "1M19840R",
    "nombre_asegurado": "ISIDRO RAMOS CRUZ",
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

    # %% Limpieza del JSON%%
json_limpiado = functionData.limpiar_json(json_str)

# %%Extracción de información%%
informacion_extraida = functionData.extraer_informacion(json_limpiado)

print("JSON limpiado y con acentos convertidos:")
print(json.dumps(json_limpiado,ensure_ascii=False,indent=2,sort_keys=True))

print("\nInformación extraída:")
print(informacion_extraida)
print(type(informacion_extraida))
# %%
