import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ono_ocr.recognition_worker import recognition_worker
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

@csrf_exempt
def index(request):
    template = loader.get_template('ono_ocr/views/index.html')
    return HttpResponse(template.render({}, request))

# Create your views here.
@csrf_exempt
def ocr_recognize(request):
    if request.method != "POST":
        return JsonResponse("Method not allowed", status=405, safe=False)

    try:
        req = json.loads(request.body.decode("utf-8"))
        filename = req.get("filename")
        doctype = req.get("doctype")
        file_base64 = req.get("file_base64")
        data = recognition_worker(filename, doctype, file_base64)

        return JsonResponse(
            data,
            status=200,
            safe=False
        )
    except Exception as e:
        return JsonResponse(str(e), status=500, safe=False)
    
