import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json.decoder import JSONDecodeError
from .chat_completions import chat_completions_arrastre_incapacidades
from datetime import datetime

@csrf_exempt
def generate_arrastre(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        req = json.loads(request.body.decode("utf-8"))
        empleado = req.get("no_empleado")
        serie_folio = req.get("serie_folio")
        fecha_a_partir = req.get("fecha_a_partir")
        fecha_actual = req.get("fecha_actual")
        dias_autorizados = req.get("dias_autorizados")
        tipo_incapacidad = req.get("tipo_incapacidad")
        categoria_incapacidad = req.get("categoria_incapacidad")
        tipo_nomina = req.get("tipo_nomina")
        historico_incapacidades = req.get("historico_incapacidades")
        tabla_periodos_ciclos = req.get("tabla_periodos_ciclos")

        data = {
            "no_empleado": empleado,
            "serie_folio": serie_folio,
            "fecha_a_partir": fecha_a_partir,
            "fecha_actual": fecha_actual,
            "dias_autorizados": dias_autorizados,
            "tipo_incapacidad": tipo_incapacidad,
            "categoria_incapacidad": categoria_incapacidad,
            "tipo_nomina": tipo_nomina,
            "historico_incapacidades": historico_incapacidades,
            "tabla_periodos_ciclos": tabla_periodos_ciclos,
        }

        # Data Validatation
        tipo_nomina = data['tipo_nomina']
        if tipo_nomina not in ['MENSUAL', 'SEMANAL', 'QUINCENAL']:
            return JsonResponse({"error": "El tipo de nomina no existe."}, status=404)
        fecha_a_partir = datetime.strptime(data['fecha_a_partir'], '%d/%m/%y') 
        fecha_actual = datetime.strptime(data['fecha_actual'], '%d/%m/%y')
        if fecha_a_partir > fecha_actual:
            return JsonResponse({"error": "La fecha a partir de la incapacidad está en el futuro."}, status=400)
        if len(data['historico_incapacidades']) != 0:
            fecha_hasta_incapacidad = datetime.strptime(data['historico_incapacidades'][0]['fecha_hasta_incapacidad'], '%d/%m/%y') 
            if fecha_hasta_incapacidad > fecha_a_partir :
                return JsonResponse({"error": "La fecha a partir de la incapacidad esta fuera de rango"}, status=400)
            
        # Process the data and perform necessary operations
        response, tokens, context = chat_completions_arrastre_incapacidades(str(data))

        return JsonResponse({"message": "Success", "response": response}, status=200)

    except JSONDecodeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
