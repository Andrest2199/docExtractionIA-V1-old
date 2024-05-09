# %% openai chat completions

import os
import sys
from openai import OpenAI
from django.conf import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ono_ocr.utils import Utils, FileUtils

# OpenAI API Key
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
api_key = settings.OPENAI_API_KEY


def chat_completions_arrastre_incapacidades(data):
    # Set data for system from folder 'Data inject'
    context_data_inyection = ""
    input_results_inicial_list = []
    input_data_inicial_list = []
    input_results_sub_list = []
    input_data_sub_list = []
    results_ini_count = 0
    results_sub_count = 0
    data_ini_count = 0
    data_sub_count = 0
    all_data_inject_files = []

    # Retrieve files from 'Data Inject'
    data_inject_folder = os.path.join(os.getcwd(), 'data_inject')
    all_data_inject_files = FileUtils.get_paths(data_inject_folder, 1)
    
    for file in all_data_inject_files:
        file_name = os.path.basename(file)
        if file_name.startswith("result_inicial"):
            input_results_inicial_list.append(FileUtils.read(file))
            results_ini_count += 1
        elif file_name.startswith("data_inicial"):
            input_data_inicial_list.append(FileUtils.read(file))
            data_ini_count += 1
        elif file_name.startswith("result_sub"):
            input_results_sub_list.append(FileUtils.read(file))
            results_sub_count += 1
        elif file_name.startswith("data_sub"):
            input_data_sub_list.append(FileUtils.read(file))
            data_sub_count += 1
        else:
            print(f"File {file} not recognized")

    # Set context data
    context_data_inyection += """
    Eres un operador de recursos humanos que analiza y registra información de incapacidades de empleados.
    Tu rol es analizar información de incapacidades, asignar días autorizados de incapacidad al periodo de la nómina del empleado y registrar la información de la incapacidad.
    A continuación te compartiremos las definiciones y lógica para llevar a cabo tu tarea.
    
    *Definición de fechas:*
    'Fecha_a_partir': Fecha donde el IMSS registra que empieza la incapacidad.
    'Fecha_actual': Fecha que el operador de recursos humanos recibe el documento de la incapacidad del empleado.
    'Fecha_inicio': El rango de fecha de principio del periodo de nómina.
    'Fecha_final': El rango de fecha de terminación del periodo de nómina.
    
    *Definición variables:*
    'Maximo_dias_aplicar': El número máximo de días de incapacidad posibles que se pueden aplicar en un periodo, está dado por la siguiente fórmula: 'maximo_dias_aplicar' = 'fecha_final' - 'fecha_inicio'
    'Días_disponibles': El número de días de incapacidad restantes disponibles que se pueden aplicar en un periodo, está dado por la siguiente fórmula: 'dias_disponibles' = 'fecha_final' - 'fecha_actual'
    
    *Definición períodos de nómina:*
    Cada periodo de nómina tiene un rango de 'fecha_inicio' y 'fecha_final'.
    Los periodos de la nómina tienen dos fases: 1) 'abiertos' o 2) 'cerrados'.
    Existen tres tipos de periodos de nóminas 1) 'mensual', 2) 'quincenal' y 3) 'semanal'.
    En periodos de nóminas 'mensuales' se pueden asignar hasta 31 días de incapacidad, dependiendo del mes en curso considerando años bisiestos.
    En periodos de nóminas 'quincenales' se pueden asignar hasta 16 días de incapacidad, dependiendo de la quincena actual. Los días totales del mes se dividen entre dos, si el número de días en el mes es par, asignas mismo número de días para cada quincena, si es non, asigna el día residuo a la segunda quincena del mes.
    En periodos de nóminas 'semanales' se pueden asignar hasta 7 días de incapacidad.
    'periodo_actual': El periodo de nómina en curso. La fecha del dia de hoy está dentro del rango 'fecha_inicio' y 'fecha_final'.
    'periodo_subsecuente': Los periodos de nómina posteriores al 'periodo_actual'.

    *Lógica asignación de días autorizados de incapacidad a periodos de nómina:*
    Existen tres 'tipo_de_incapacidad': 1) Enfermedad General (EG), 2) Maternidad (MT), 3) Riesgo de Trabajo (AT)
    Existen dos 'categorías_de_incapacidades' 1) Inicial y 2) Subsecuente
    Los 'dias_autorizados' son los días de incapacidad que autorizó el Instituto Mexicano de Seguridad Social.
    Los 'dias_autorizados' se asignan al 'periodo_actual' y a 'periodo_subsecuentes'. Siempre y cuando el periodo de la nómina en curso se encuentre en fase abierto.
    Los 'dias_autorizados' se asignan contando días naturales no en días laborales. Es decir se consideran días festivos y fines de semana.
    Los 'diaz_autorizados' a asignar al periodo correspondiente no deben de exceder los 'dias_disponibles' y/o el 'maximo_dias_aplicar'.
    En el JSON de 'empleados_incapacidades' buscar si la incapacidad existe por 'no_empleado' o 'serie_y_folio'. Si no existe, elaborará el registro con todas las validaciones correspondientes. Si existe verifica que la información esté correcta.
    En el JSON de 'periodos_ciclos' buscar el 'periodo_actual' correspondiente. Para encontrar el 'periodo_actual', la 'fecha_actual' de la incapacidad debe estar dentro del rango de 'fecha_inicio' y "fecha_final" del 'periodo_actual'.
    Válida en qué fase está el periodo. Si la fase de ese periodo está abierta, empieza a asignar los 'dias_autorizados' al periodo, de lo contrario, asigna los 'dias_autorizados' al periodo subsecuente.
    Si la 'fecha_a_partir' es posterior a la 'fecha_actual', manda un mensaje de error que la incapacidad está en el futuro.
    Si la cantidad de 'días_autorizados' es menor o igual a la cantidad de 'dias_disponibles' en el periodo actual, se asignan los días autorizados al periodo_actual.
    Si la cantidad de 'dias_autorizados' es mayor a la cantidad de 'dias_disponibles' en el periodo actual, se asignan los 'días_autorizados' al 'máximo_dias_aplicar' del 'periodo_actua'l y los días restantes al 'periodo_subsecuente', y si este restante excede el 'maximo_dias_aplicar' del 'periodo_subsecuent'e, se asigna el 'maximo_dias_aplicar' y el remanente al 'periodo_subsecuente', y así sucesivamente.\n\n
    """

    context_data_inyection += f"Entre xml tags se te proporcionan {len(input_data_inicial_list)} ejemplos input y output de asignacion de dias de incapacidad iniciales a periodos de nómina:\n\n"
    data_count = 1
    results_count = 1
    for input_data, input_result in zip(input_data_inicial_list, input_results_inicial_list):
        context_data_inyection += f"<input_incapacidad_inicial_ejemplo_{data_count}>\n\n{input_data}\n\n</input_incapacidad_inicial_ejemplo_{data_count}>\n\n<output_incapacidad_inicial_ejemplo_{results_count}>\n\n{input_result}\n\n</output_incapacidad_inicial_ejemplo_{results_count}>\n\n"
        data_count += 1
        results_count += 1

    context_data_inyection += f"Entre xml tags se te proporcionan {len(input_data_sub_list)} ejemplos input y output de incapacidades subsecuentes:\n\n"
    data_count = 1
    results_count = 1
    for input_data, input_result in zip(input_data_sub_list, input_results_sub_list):
        context_data_inyection += f"<input_incapacidad_subsecuente_ejemplo_{data_count}>\n\n{input_data}\n\n</input_incapacidad_subsecuente_ejemplo_{data_count}>\n\n<output_incapacidad_subsecuente_ejemplo_{results_count}>\n\n{input_result}\n\n</output_incapacidad_subsecuente_ejemplo_{results_count}>\n\n"
        data_count += 1
        results_count += 1

    context_data_inyection += """
    *Decripción de información que recibirás del usuario en formato JSON:*\n
    Datos de la nueva incapacidad a registrar.\n
    Una lista de periodos de nómina con tipo de nómina, rango de fechas del periodo, días por periodo y su estatus abierto o cerrado.\n
    Una lista del historial de incapacidades registrados.\n\n
   
    *Crea un JSON output que tenga la siguiente estructura de información:*

    {
        "no_empleado": str,
        "serie_folio": str,
        "tipo_incapacidad": str (inicial|subsecuente),
        "fecha_desde": date str,
        "fecha_hasta": date str,
        "dias_autorizados": int,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": str,
                    "dias_aplicados": int
                    },
                { 
                    "periodo_nomina": str,
                    "dias_aplicados": int}
            ]
    }
    """
    # Set system role
    system_content = {"role": "system", "content": context_data_inyection}
    # Set user role
    user_content = {"role": "user", "content": data}

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

    tokens_count = response.usage.prompt_tokens

    return json_data, tokens_count, context_data_inyection

# %% Run chat completions

data_inicial = {
    "no_empleado": "2811",
    "serie_folio": "123456",
    "fecha_a_partir": "22/04/24",
    "fecha_actual": "23/04/24",
    "dias_autorizados": "DIEZ",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "periodo": "20240401",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "30/04/24",
            "estatus_del_periodo": "ABIERTO"
        },
        {
            "periodo": "20240501",
            "fecha_desde": "01/05/24",
            "fecha_hasta": "31/05/24",
            "estatus_del_periodo": "ABIERTO"
        },
        {
            "periodo": "20240601",
            "fecha_desde": "01/06/24",
            "fecha_hasta": "30/06/24",
            "estatus_del_periodo": "ABIERTO"
        },
        {
            "periodo": "20240701",
            "fecha_desde": "01/07/24",
            "fecha_hasta": "31/07/24",
            "estatus_del_periodo": "ABIERTO"
        }
    ]
}

# result_inicial, tokens, context = chat_completions_arrastre_incapacidades(str(data_inicial))