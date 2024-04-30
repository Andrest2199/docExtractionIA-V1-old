# %% data injecy samples

import json
import os

folder_base_path = os.getcwd()

# %% Incapacidades iniciales

# incapacidad inicial 1 / nomina quincenal / asignación en 1 periodo
data_inicial_1 = {
    "no_empleado": "2691",
    "serie_folio": "MS736601",
    "fecha_a_partir": "09/03/24",
    "fecha_actual": "16/03/24",
    "dias_autorizados": "TRES",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "15/03/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240302",
            "fecha_desde": "15/03/24",
            "fecha_hasta": "31/03/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240401",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "15/04/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240402",
            "fecha_desde": "15/04/24",
            "fecha_hasta": "30/04/24",
        },
    ],
}

result_inicial_1 = {
    "no_empleado": "2691",
    "serie_folio": "MS736601",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "09/03/24",
    "fecha_hasta": "11/03/24",
    "dias_autorizados": 3,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240302", "dias_aplicados": 3}
    ],
}

# incapacidad inicial 2 / nomina quincenal / asignación en multiples periodos
data_inicial_2 = {
    "no_empleado": "1499",
    "serie_folio": "MQ778848",
    "fecha_a_partir": "28/01/24",
    "fecha_actual": "03/02/24",
    "dias_autorizados": "VEINTIOCHO",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240201",
            "fecha_desde": "01/02/24",
            "fecha_hasta": "15/02/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240202",
            "fecha_desde": "15/02/24",
            "fecha_hasta": "28/02/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "15/04/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240302",
            "fecha_desde": "15/03/24",
            "fecha_hasta": "31/03/24",
        },
    ],
}

result_inicial_2 = {
    "no_empleado": "1499",
    "serie_folio": "MQ778848",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "28/01/24",
    "fecha_hasta": "24/02/24",
    "dias_autorizados": 28,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240201", "dias_aplicados": 15},
        {"periodo_nomina": "20240202", "dias_aplicados": 13},
    ],
}

# incapacidad inicial 3 / nomina mensual / asignación en 1 periodo
data_inicial_3 = {
    "no_empleado": "2477",
    "serie_folio": "YC255144",
    "fecha_a_partir": "08/03/24",
    "fecha_actual": "20/03/24",
    "dias_autorizados": "CINCO",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "31/03/24",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240401",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "30/04/24",
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240501',
            'fecha_desde': '01/05/24',
            'fecha_hasta': '31/05/24',
        },
    ],
}

result_inicial_3 = {
    "no_empleado": "2477",
    "serie_folio": "YC255144",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "08/03/24",
    "fecha_hasta": "10/03/24",
    "dias_autorizados": 3,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240301", "dias_aplicados": 3}
    ],
}

# incapacidad inicial 4 / nomina mensual / asignación en multiples periodos
data_inicial_4 = {
    "no_empleado": "2232",
    "serie_folio": "MK879939",
    "fecha_a_partir": "28/11/23",
    "fecha_actual": "01/12/23",
    "dias_autorizados": "OCHENTA Y CUATRO",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20231101",
            "fecha_desde": "01/11/23",
            "fecha_hasta": "30/11/23",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20231201",
            "fecha_desde": "01/12/23",
            "fecha_hasta": "31/12/23",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240101",
            "fecha_desde": "01/01/24",
            "fecha_hasta": "31/01/24",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240201",
            "fecha_desde": "01/02/24",
            "fecha_hasta": "29/02/24",
        },
    ],
}

result_inicial_4 = {
    "no_empleado": "2232",
    "serie_folio": "MK879939",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "28/11/23",
    "fecha_hasta": "19/28/24",
    "dias_autorizados": 84,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20231201", "dias_aplicados": 31},
        {"periodo_nomina": "20240101", "dias_aplicados": 31},
        {"periodo_nomina": "20240201", "dias_aplicados": 22},
    ],
}

# TODO: incapacidad inicial 5 / nomina semanal / asignación en 1 periodo
data_inicial_5 = {
    "no_empleado": "2705",
    "serie_folio": "MS736651",
    "fecha_a_partir": "16/03/24",
    "fecha_actual": "02/04/24",
    "dias_autorizados": "TRES",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "SEMANAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240304",
            "fecha_desde": "25/03/24",
            "fecha_hasta": "31/03/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240401",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "07/04/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240402",
            "fecha_desde": "08/04/24",
            "fecha_hasta": "14/04/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240403",
            "fecha_desde": "15/04/24",
            "fecha_hasta": "21/04/24",
        },
    ],
}

result_inicial_5 = {
    "no_empleado": "2705",
    "serie_folio": "MS736651",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "16/03/24",
    "fecha_hasta": "18/03/24",
    "dias_autorizados": 3,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240401", "dias_aplicados": 3}
    ],
}

# Incapacidad inicial 6 / nomina semanal / asignación en multiples periodos
data_inicial_6 = {
    "no_empleado": "2538",
    "serie_folio": "MO571502",
    "fecha_a_partir": "14/03/24",
    "fecha_actual": "02/04/24",
    "dias_autorizados": "OCHO",
    "tipo_incapacidad": "INICIAL",
    "tipo_nomina": "SEMANAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240304",
            "fecha_desde": "25/03/24",
            "fecha_hasta": "31/03/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240401",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "07/04/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240402",
            "fecha_desde": "08/04/24",
            "fecha_hasta": "14/04/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240403",
            "fecha_desde": "15/04/24",
            "fecha_hasta": "21/04/24",
        },
    ],
}

result_inicial_6 = {
    "no_empleado": "2538",
    "serie_folio": "MO571502",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "14/03/24",
    "fecha_hasta": "21/03/24",
    "dias_autorizados": 8,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240401", "dias_aplicados": 7},
        {"periodo_nomina": "20240402", "dias_aplicados": 1},
    ],
}

# %% Incapacidades subsecuentes
data_sub_1 = {
    "no_empleado": "1467",
    "serie_folio": "QP628808",
    "fecha_a_partir": "21/12/23",
    "fecha_actual": "22/12/23",
    "dias_autorizados": "SIETE",
    "tipo_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [
        {
            "no_empleado": "1467",
            "serie_folio": "MK878347",
            "tipo_incapacidad": "INICIAL",
            "fecha_desde": "20/12/23",
            "fecha_hasta": "20/12/23",
            "dias_autorizados": 1,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "20231202", "dias_aplicados": 1}
            ],
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20231201",
            "fecha_desde": "01/12/23",
            "fecha_hasta": "15/12/23",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20231202",
            "fecha_desde": "15/12/23",
            "fecha_hasta": "31/12/23",
        },
    ],
}


data_sub_2 = {
    "no_empleado": "1499",
    "serie_folio": "VL240491",
    "fecha_a_partir": "25/02/24",
    "fecha_actual": "30/03/24",
    "dias_autorizados": "CINCO",
    "tipo_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [
        {
            "no_empleado": "1499",
            "serie_folio": "MQ778848",
            "tipo_incapacidad": "INICIAL",
            "fecha_desde": "28/01/24",
            "fecha_hasta": "24/02/24",
            "dias_autorizados": 28,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "2024021", "dias_aplicados": 15},
                {"periodo_nomina": "2024022", "dias_aplicados": 13},
            ],
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240202",
            "fecha_desde": "15/02/24",
            "fecha_hasta": "29/02/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "15/03/24",
        },
        {
            "descripcion_nomina": "QUINCENAL",
            "periodo": "20240302",
            "fecha_desde": "15/03/24",
            "fecha_hasta": "31/03/24",
        },
    ],
}

data_sub_3 = {
    "no_empleado": "2561",
    "serie_folio": "UN035361",
    "fecha_a_partir": "25/01/24",
    "fecha_actual": "29/01/24",
    "dias_autorizados": "OCHO",
    "tipo_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [
        {
            "no_empleado": "2561",
            "serie_folio": "UN035369",
            "tipo_incapacidad": "INICIAL",
            "fecha_desde": "22/01/24",
            "fecha_hasta": "24/01/24",
            "dias_autorizados": 3,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "20240201", "dias_aplicados": 3}
            ],
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240101",
            "fecha_desde": "01/01/24",
            "fecha_hasta": "31/01/24",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240201",
            "fecha_desde": "01/02/24",
            "fecha_hasta": "29/02/24",
        },
        {
            "descripcion_nomina": "MENSUAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "31/03/24",
        },
    ],
}

data_sub_4 = {
    "no_empleado": "1299",
    "serie_folio": "PKF32361",
    "fecha_a_partir": "14/02/24",
    "fecha_actual": "21/02/24",
    "dias_autorizados": "OCHO",
    "tipo_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "SEMANAL",
    "historico_incapacidades": [
        {
            "no_empleado": "1299",
            "serie_folio": "PKF33362",
            "tipo_incapacidad": "INICIAL",
            "fecha_desde": "10/02/24",
            "fecha_hasta": "13/02/24",
            "dias_autorizados": 4,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "20240201", "dias_aplicados": 4}
            ],
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240202",
            "fecha_desde": "08/02/24",
            "fecha_hasta": "14/02/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240203",
            "fecha_desde": "15/02/24",
            "fecha_hasta": "22/02/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240204",
            "fecha_desde": "23/02/24",
            "fecha_hasta": "29/02/24",
        },
        {
            "descripcion_nomina": "SEMANAL",
            "periodo": "20240301",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "07/03/24",
        },
    ],
}

result_sub_1 = {
    "no_empleado": "1467",
    "serie_folio": "QP628808",
    "tipo_incapacidad": "SUBSECUENTE",
    "fecha_desde": "21/12/23",
    "fecha_hasta": "17/12/23",
    "dias_autorizados": 7,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20231202", "dias_aplicados": 7}
    ],
}

result_sub_2 = {
    "no_empleado": "1499",
    "serie_folio": "VL240491",
    "tipo_incapacidad": "SUBSECUENTE",
    "fecha_desde": "25/02/24",
    "fecha_hasta": "29/02/24",
    "dias_autorizados": 5,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240202", "dias_aplicados": 5}
    ],
}

result_sub_3 = {
    "no_empleado": "2561",
    "serie_folio": "UN035361",
    "tipo_incapacidad": "SUBSECUENTE",
    "fecha_desde": "25/01/24",
    "fecha_hasta": "01/02/24",
    "dias_autorizados": 8,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240101", "dias_aplicados": 7},
        {"periodo_nomina": "20240201", "dias_aplicados": 1},
    ],
}

result_sub_4 = {
    "no_empleado": "1299",
    "serie_folio": "PKF32361",
    "tipo_incapacidad": "INICIAL",
    "fecha_desde": "14/02/24",
    "fecha_hasta": "21/02/24",
    "dias_autorizados": 8,
    "dias_incapacidad_aplicados_a_periodos": [
        {"periodo_nomina": "20240202", "dias_aplicados": 1},
        {"periodo_nomina": "20240203", "dias_aplicados": 7},
    ],
}
# %% Save as json

# Define the list of variables to save as json files
json_files_list = [
    "data_inicial_1",
    "result_inicial_1",
    "data_inicial_2",
    "result_inicial_2",
    "data_inicial_3",
    "result_inicial_3",
    "data_inicial_4",
    "result_inicial_4",
    "data_sub_1",
    "result_sub_1",
    "data_sub_2",
    "result_sub_2",
    "data_sub_3",
    "result_sub_3",
    "data_sub_4",
    "result_sub_4",
]  # 'data_inicial_5', 'result_inicial_5', 'data_inicial_6', 'result_inicial_6'

# Save each variable as a json file
for file in json_files_list:
    if file in globals():
        file_path = os.path.join(folder_base_path, f"data_inject/{file}.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(globals()[file], f, indent=4)
    else:
        print(f"Variable {file} is not defined.")

# %%
