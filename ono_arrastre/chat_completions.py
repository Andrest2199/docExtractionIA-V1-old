# %% openai chat completions
import os
from openai import OpenAI
from ono_ocr.utils import Utils,FileUtils
# from django.conf import settings

# OpenAI API Key
# api_key = settings.OPENAI_API_KEY


def chat_completions(data):
    # Set Data for system from folder 'Data inject'
    context_data_inyection = ""
    input_results_inicial_list,input_data_inicial_list,input_results_sub_list,input_data_sub_list = []
    results_ini_count,results_sub_count,data_ini_count,data_sub_count = 0
    all_data_inject_files = []

    # Retrieve files from 'Data Inject'
    data_inject_folder = os.getcwd+'/data_inject'
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
    context_data_inyection = f"Eres un operador de recursos humanos que analiza y registra información de incapacidades de empleados. 
        Tu rol es analizar información de incapacidades, asignar días autorizados de incapacidad al periodo de la nómina del empleado y registrar la información de la incapacidad.
        A continuación te compartiremos las definiciones y lógica para llevar a cabo tu tarea.
        Definición de fechas:
        'Fecha_a_partir': Fecha donde el IMSS registra que empieza la incapacidad
        'Fecha_actual': Fecha que el operador de recursos humanos recibe el documento de la incapacidad del empleado
        'Fecha_inicio': El rango de fecha de principio del periodo de nómina
        'Fecha_final': El rango de fecha de terminación del periodo de nómina
        Definición variables:
        'Maximo_dias_aplicar': El número máximo de días posibles que se pueden aplicar en un periodo, está dado por la siguiente fórmula: 'Fecha_final' - 'Fecha_inicio'
        'Días_disponibles': El número de días restantes disponibles que se pueden aplicar en un periodo, está dado por la siguiente fórmula: 'Fecha_final' - 'Fecha_actual'
        Definiciones y lógica general:
        Existen tres tipos de incapacidad: 1) Enfermedad General (EG), 2) Maternidad (MT), 3) Riesgo de Trabajo (AT).
        Existen dos categorías de incapacidades 1) Inicial y 2) Subsecuente.
        Existen tres tipos de nóminas 1) Mensual, 2) Quincenal y 3) Semanal.
        Las incapacidades se asignan en días naturales no en días laborales. Es decir se consideran festivos y fines de semana.
        En nóminas mensuales se pueden asignar hasta 31 días de incapacidad, dependiendo del mes en curso considerando años bisiestos.
        En nóminas quincenales se pueden asignar hasta 16 días de incapacidad, dependiendo de la quincena actual. Los días totales del mes se dividen entre dos, si el número de días en el mes es par, asignas mismo número de días para cada quincena, si es non, asigna el día residuo a la segunda quincena del mes.
        En nóminas semanales se pueden asignar hasta 7 días de incapacidad.
        Un periodo tiene un rango de 'fecha_inicio' y 'fecha_final'. 
        El periodo comprende el tiempo desde la 'fecha_inicio' hasta la 'fecha_final'.
        Los periodos de la nómina pueden estar abiertos o cerrados.
        Se pueden asignar días de incapacidad autorizados al periodo en curso y a periodos subsecuentes, siempre y cuando el periodo de la nómina en curso se encuentre abierto.
        Si se aplica un máximo de días, dependiendo del número de días autorizados revisar que no se apliquen más de lo debido en el periodo.
        Los días de incapacidad autorizados se aplican al periodo actual y a periodos subsecuentes. 
        En el JSON de 'empleados_incapacidades' buscar si la incapacidad existe por 'no_empleado' o 'serie_y_folio'. Si no existe, elaborarás el registro con todas las validaciones correspondientes. Si existe verifica que la información esté correcta.
        En el JSON de 'periodos_ciclos' buscar el periodo correspondiente. Para encontrar el periodo, la 'fecha_a_partir' de la incapacidad debe estar dentro del rango de 'fecha_inicio' y 'fecha_final'. 
        Y considerar en qué fase está el periodo. Si la fase de ese periodo está abierta, considerar ese periodo, de lo contrario, considerar el periodo subsecuente.
        Si la cantidad de días autorizados es menor o igual a la cantidad de días disponibles en el periodo actual (días disponibles = fecha final - fecha actual), se asignan los días autorizados al periodo actual.
        Si la cantidad de días autorizados es mayor a la cantidad de días disponibles en el periodo actual (días disponibles = fecha final - fecha actual), se asignan los días autorizados al máximo disponible del periodo actual y los días restantes al periodo subsecuente, y si este restante excede el máximo disponible del periodo subsecuente, se asigna el máximo disponible y el remanente al siguiente periodo, y así sucesivamente.
        \nEntre xml tags se te proporcionan {data_ini_count} ejemplos input y output de incapacidades iniciales:
        \n\n"

    data_count = 1
    results_count = 1
    for input_data, input_result in zip(input_data_inicial_list, input_results_inicial_list):
        context_data_inyection += f"<data_input_example_inicial_{data_count}>\n\n{input_data}\n\n</data_input_example_inicial_{data_count}>\n\n<result_output_example_inicial_{results_count}>\n\n{input_result}\n\n</result_output_example_inicial_{results_count}>\n\n"
        data_count += 1
        results_count += 1

    context_data_inyection += "\nEntre xml tags se te proporcionan {n} ejemplos input y output de incapacidades subsecuentes:\n\n"
    data_count = 1
    results_count = 1
    for input_data, input_result in zip(input_data_sub_list, input_results_sub_list):
        context_data_inyection += f"<data_input_example_subsecuente_{data_count}>\n\n{input_data}\n\n</data_input_example_subsecuente_{data_count}>\n\n<result_output_example_subsecuente_{results_count}>\n\n{input_result}\n\n</result_output_example_subsecuente_{results_count}>\n\n"
        data_count += 1
        results_count += 1

    context_data_inyection += "Información que recibirás del usuario en formato JSON: Una lista de periodos de nómina con tipo de nómina, rango de fechas del periodo, días por periodo y su estatus abierto o cerrado. Una lista del historial de incapacidades registrados llamada empleados_incapacidades.Datos de la nueva incapacidad a registrar.Tu tarea es analizar y registrar la nueva incapacidad y crear un JSON output usando el siguiente formato JSON:\n\n"
    context_data_inyection += """
    {
        "no_empleado": string,
        "serie_folio": string,
        "tipo_incapacidad": string (inicial|subsecuente),
        "fecha_desde": date string,
        "fecha_hasta": date string,
        "dias_autorizados": integer,
        "periodos_aplicados_\{n\}": {
            0:  { "dias_aplicados": integer,
                "periodo_aplicado": integer},
            ...,

            \{n\}: { "dias_aplicados": integer,
                "periodo_aplicado": integer}
        }
    }
    Donde '\{n\}' es el numero de periodos que se aplicaron dias de incapacidad.
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
    # json_data = json.loads(json_string)
    json_data = Utils.to_dict(json_string)

    tokens_count_by_gpt = response.usage.prompt_tokens

    return json_data
