# %% data injecy samples

import json

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
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240301',
            'fecha_desde': '01/03/24',
            'fecha_hasta': '15/03/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240302',
            'fecha_desde': '15/03/24',
            'fecha_hasta': '31/03/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240401',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '15/04/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240402',
            'fecha_desde': '15/04/24',
            'fecha_hasta': '30/04/24',
        },
    ]
}

result_inicial_1 = {
        "no_empleado": "2691",
        "serie_folio": "MS736601",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "09/03/24",
        "fecha_hasta": "11/03/24",
        "dias_autorizados": 3,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20240302",
                    "dias_aplicados": 3
                    }
            ]
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
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240201',
            'fecha_desde': '01/02/24',
            'fecha_hasta': '15/02/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240202',
            'fecha_desde': '15/02/24',
            'fecha_hasta': '28/02/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240301',
            'fecha_desde': '01/03/24',
            'fecha_hasta': '15/04/24',
        },
        {
            'descripcion_nomina': 'QUINCENAL',
            'periodo': '20240302',
            'fecha_desde': '15/03/24',
            'fecha_hasta': '31/03/24',
        },
    ]
}

result_inicial_2 = {
        "no_empleado": "1499",
        "serie_folio": "MQ778848",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "28/01/24",
        "fecha_hasta": "24/02/24",
        "dias_autorizados": 28,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20240201",
                    "dias_aplicados": 15
                    },
                {
                    "periodo_nomina": "20240202",
                    "dias_aplicados": 13
                    }
            ]
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
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240301',
            'fecha_desde': '01/03/24',
            'fecha_hasta': '31/03/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240401',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '30/04/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240501',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '31/04/24',
        },
    ]
}

result_inicial_3 = {
        "no_empleado": "2477",
        "serie_folio": "YC255144",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "08/03/24",
        "fecha_hasta": "10/03/24",
        "dias_autorizados": 3,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20240301",
                    "dias_aplicados": 3
                    }
            ]
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
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20231101',
            'fecha_desde': '01/11/23',
            'fecha_hasta': '30/11/23',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20231201',
            'fecha_desde': '01/12/23',
            'fecha_hasta': '31/12/23',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240101',
            'fecha_desde': '01/01/24',
            'fecha_hasta': '31/01/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240201',
            'fecha_desde': '01/02/24',
            'fecha_hasta': '29/02/24',
        },
    ]
}

result_inicial_4 = {
        "no_empleado": "2232",
        "serie_folio": "MK879939",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "28/11/23",
        "fecha_hasta": "19/28/24",
        "dias_autorizados": 84,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20231201",
                    "dias_aplicados": 31
                    },
                {
                    "periodo_nomina": "20240101",
                    "dias_aplicados": 31
                    },
                {
                    "periodo_nomina": "20240201",
                    "dias_aplicados": 22
                    }
            ]
}

# TODO: incapacidad inicial 5 / nomina semanal / asignación en 1 periodo
data_inicial_5 = {
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
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240301',
            'fecha_desde': '01/03/24',
            'fecha_hasta': '31/03/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240401',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '30/04/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240501',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '31/04/24',
        },
    ]
}

result_inicial_5 = {
        "no_empleado": "2477",
        "serie_folio": "YC255144",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "08/03/24",
        "fecha_hasta": "10/03/24",
        "dias_autorizados": 3,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20240301",
                    "dias_aplicados": 3
                    }
            ]
}

# TODO: incapacidad inicial 6 / nomina semanal / asignación en multiples periodos
data_inicial_6 = {
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
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240301',
            'fecha_desde': '01/03/24',
            'fecha_hasta': '31/03/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240401',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '30/04/24',
        },
        {
            'descripcion_nomina': 'MENSUAL',
            'periodo': '20240501',
            'fecha_desde': '01/04/24',
            'fecha_hasta': '31/04/24',
        },
    ]
}

result_inicial_6 = {
        "no_empleado": "2477",
        "serie_folio": "YC255144",
        "tipo_incapacidad": "INICIAL",
        "fecha_desde": "08/03/24",
        "fecha_hasta": "10/03/24",
        "dias_autorizados": 3,
        "dias_incapacidad_aplicados_a_periodos": 
            [
                {
                    "periodo_nomina": "20240301",
                    "dias_aplicados": 3
                    }
            ]
}






