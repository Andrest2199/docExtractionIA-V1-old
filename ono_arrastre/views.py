import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json.decoder import JSONDecodeError


@csrf_exempt
def generate_arrastre(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        req = json.loads(request.body.decode("utf-8"))
        empleado = req.get("empleado")
        serie_folio = req.get("serie_folio")
        fecha_a_partir = req.get("fecha_a_partir")
        fecha_actual = req.get("fecha_actual")
        dias_autorizados = req.get("dias_autorizados")
        tipo_incapacidad = req.get("tipo_incapacidad")
        tipo_nomina = req.get("tipo_nomina")
        historico_incapacidades = req.get("historico_incapacidades")
        tabla_periodos_ciclos = req.get("tabla_periodos_ciclos")

        data = {
            "empleado": empleado,
            "serie_folio": serie_folio,
            "fecha_a_partir": fecha_a_partir,
            "fecha_actual": fecha_actual,
            "dias_autorizados": dias_autorizados,
            "tipo_incapacidad": tipo_incapacidad,
            "tipo_nomina": tipo_nomina,
            "historico_incapacidades": historico_incapacidades,
            "tabla_periodos_ciclos": tabla_periodos_ciclos,
        }

        # Process the data and perform necessary operations

        return JsonResponse({"message": "Success"}, status=200)

    except JSONDecodeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
