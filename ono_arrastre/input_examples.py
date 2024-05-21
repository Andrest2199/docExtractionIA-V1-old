# EXAMPLE INICIAL 1 / NOMINA QUINCENAL CHECK
{
    "no_empleado": "1666",
    "serie_folio": "WG336076",
    "fecha_a_partir": "20/08/21",
    "fecha_actual": "20/08/21",
    "dias_autorizados": "TRES",
    "tipo_incapacidad": "EG",
    "categoria_incapacidad": "INICIAL",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "periodo": "2021081",
            "fecha_desde": "01/08/21",
            "fecha_hasta": "15/08/21",
            "fase": "CERRADO"
        },
        {
            "periodo": "2021082",
            "fecha_desde": "15/08/21",
            "fecha_hasta": "31/08/21",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2021091",
            "fecha_desde": "01/09/21",
            "fecha_hasta": "15/09/21",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2021092",
            "fecha_desde": "15/09/21",
            "fecha_hasta": "30/09/21",
            "fase": "ABIERTO"
        }
    ],
    "auth_fase_cerrada": "False"
},

# RESULT INICIAL 1 / NOMINA QUINCENAL CHECK
{
    "message": "Success",
    "response": {
        "no_empleado": "1666",
        "serie_folio": "WG336076",
        "tipo_incapacidad": "EG",
        "categoria_incapacidad": "inicial",
        "fecha_desde_incapacidad": "20/08/21",
        "fecha_hasta_incapacidad": "22/08/21",
        "fecha_desde_aplicado_nomina": "20/08/21",
        "fecha_hasta_aplicado_nomina": "22/08/21",
        "dias_autorizados": 3,
        "dias_incapacidad_aplicados_a_periodos": [
            {
                "periodo_nomina": "2021082",
                "dias_aplicados": 3
            }
        ]
    }
}
# EXAMPLE INICIAL 2 / NOMINA MENSUAL CHECK
{
    "no_empleado": "2345",
    "serie_folio": "WX321288",
    "fecha_a_partir": "20/03/24",
    "fecha_actual": "15/04/24",
    "dias_autorizados": "VEINTE",
    "tipo_incapacidad": "MT",
    "categoria_incapacidad": "INICIAL",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [],
    "tabla_periodos_ciclos": [
        {
            "periodo": "2024031",
            "fecha_desde": "01/03/24",
            "fecha_hasta": "31/03/24",
            "fase": "CERRADO"
        },
        {
            "periodo": "2024041",
            "fecha_desde": "01/04/24",
            "fecha_hasta": "30/04/24",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2024051",
            "fecha_desde": "01/05/24",
            "fecha_hasta": "31/05/24",
            "fase": "ABIERTO"
        }
    ],
    "auth_fase_cerrada": "False"
},
# EXAMPLE SUBSECUENTE 1 / NOMINA QUINCENAL CHECK
{
    "no_empleado": "1666",
    "serie_folio": "WG336205",
    "fecha_a_partir": "23/08/21",
    "fecha_actual": "23/08/21",
    "dias_autorizados": "CATORCE",
    "categoria_incapacidad": "SUBSECUENTE",
    "tipo_incapacidad": "EG",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [
        {
            "no_empleado": "1666",
            "serie_folio":"WG336076",
            "tipo_incapacidad":"EG",
            "fecha_desde_incapacidad":"20/08/21",
            "fecha_hasta_incapacidad":"22/08/21",
            "fecha_desde_aplicado_nomina":"20/08/21",
            "fecha_hasta_aplicado_nomina":"22/08/21",   
            "dias_autorizados": 3,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "2021082", "dias_aplicados": 3}
            ]
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "periodo": "2021081",
            "fecha_desde": "01/08/21",
            "fecha_hasta": "15/08/21",
            "fase": "CERRADO"
        },
        {
            "periodo": "2021082",
            "fecha_desde": "16/08/21",
            "fecha_hasta": "31/08/21",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2021091",
            "fecha_desde": "01/09/21",
            "fecha_hasta": "15/09/21",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2021092",
            "fecha_desde": "16/09/21",
            "fecha_hasta": "30/09/21",
            "fase": "ABIERTO"
        }
    ],
    "auth_fase_cerrada": "False"
}
#Result
{
    "message": "Success",
    "response": {
        "no_empleado": "1666",
        "serie_folio": "WG336205",
        "tipo_incapacidad": "EG",
        "categoria_incapacidad": "SUBSECUENTE",
        "fecha_desde_incapacidad": "23/08/21",
        "fecha_hasta_incapacidad": "05/09/21",
        "fecha_desde_aplicado_nomina": "23/08/21",
        "fecha_hasta_aplicado_nomina": "05/09/21",
        "dias_autorizados": 14,
        "dias_incapacidad_aplicados_a_periodos": [
            {
                "periodo_nomina": "2021082",
                "dias_aplicados": 9
            },
            {
                "periodo_nomina": "2021091",
                "dias_aplicados": 5
            }
        ]
    }
}
# EXAMPLE SUBSECUENTE 2 / NOMINA MENSUAL CHECK
{
    "no_empleado": "1892",
    "serie_folio": "WG337602",
    "fecha_a_partir": "06/02/24",
    "fecha_actual": "06/02/24",
    "dias_autorizados": "CATORCE",
    "tipo_incapacidad": "EG",
    "categoria_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "MENSUAL",
    "historico_incapacidades": [
        {
            "no_empleado": "1892",
            "serie_folio":"WG336205",
            "tipo_incapacidad": "EG",
            "fecha_desde_incapacidad":"02/02/24",
            "fecha_hasta_incapacidad":"05/02/24",
            "fecha_desde_aplicado_nomina":"02/02/24",
            "fecha_hasta_aplicado_nomina":"05/02/24",
            "dias_autorizados": 4,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "2024021", "dias_aplicados": 4}
            ],
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "periodo": "2023121",
            "fecha_desde": "01/12/23",
            "fecha_hasta": "31/12/23",
            "fase": "CERRADO"
        },
        {
            "periodo": "2024011",
            "fecha_desde": "01/01/24",
            "fecha_hasta": "31/01/24",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2024021",
            "fecha_desde": "01/02/24",
            "fecha_hasta": "29/02/24",
            "fase": "ABIERTO"
        }
    ],
    "auth_fase_cerrada": "False"
}
#Resutl
{
    "message": "Success",
    "response": {
        "no_empleado": "1892",
        "serie_folio": "WG337602",
        "tipo_incapacidad": "EG",
        "categoria_incapacidad": "SUBSECUENTE",
        "fecha_desde_incapacidad": "06/02/24",
        "fecha_hasta_incapacidad": "19/02/24",
        "fecha_desde_aplicado_nomina": "06/02/24",
        "fecha_hasta_aplicado_nomina": "19/02/24",
        "dias_autorizados": 14,
        "dias_incapacidad_aplicados_a_periodos": [
            {
                "periodo_nomina": "2024021",
                "dias_aplicados": 14
            }
        ]
    }
}
# EXAMPLE SUBSECUENTE 3 / NOMINA QUINCENAL
{
    "no_empleado": "2190",
    "serie_folio": "CD536241",
    "fecha_a_partir": "20/06/24",
    "fecha_actual": "10/07/24",
    "dias_autorizados": "TREINTA Y TRES",
    "tipo_incapacidad": "EG",
    "categoria_incapacidad": "SUBSECUENTE",
    "tipo_nomina": "QUINCENAL",
    "historico_incapacidades": [
        {
            "no_empleado": "2190",
            "serie_folio": "CD533361",
            "tipo_incapacidad":"EG",
            "categoria_incapacidad": "INICIAL",
            "fecha_desde_incapacidad": "15/06/24",
            "fecha_hasta_incapacidad": "18/06/24",
            "fecha_desde_aplicado_nomina": "15/06/24",
            "fecha_hasta_aplicado_nomina": "18/06/24",
            "dias_autorizados": 4,
            "dias_incapacidad_aplicados_a_periodos": [
                {"periodo_nomina": "2024062", "dias_aplicados": 4}
            ]
        }
    ],
    "tabla_periodos_ciclos": [
        {
            "periodo": "2024062",
            "fecha_desde": "16/06/24",
            "fecha_hasta": "30/06/24",
            "fase": "CERRADO"
        },
        {
            "periodo": "2024071",
            "fecha_desde": "01/07/24",
            "fecha_hasta": "15/07/24",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2024072",
            "fecha_desde": "16/07/24",
            "fecha_hasta": "31/07/24",
            "fase": "ABIERTO"
        },
        {
            "periodo": "2024081",
            "fecha_desde": "01/08/24",
            "fecha_hasta": "15/08/24",
            "fase": "ABIERTO"
        }
    ],
    "auth_fase_cerrada": "False"
}
#Comment
"""Try
# line 60: 'fecha_hasta_incapacidad': Es la suma de los 'dias_autorizados' a la 'fecha_a_partir' menos un día, esta dado por la siguiente formula: 'fecha_hasta_incapacidad' = 'fecha_a_partir' + 'dias_autorizados' - 1
# line 62: 'fecha_hasta_aplicado_nomina': Es la fecha resultante de la suma de los 'dias_autorizados' a la 'fecha_desde_aplicado_nomina', esta dado por la siguient formula: 'fecha_hasta_aplicado_nomina' = 'fecha_desde_aplicado_nomina' + 'dias_autorizados' - 1
"""
#Result