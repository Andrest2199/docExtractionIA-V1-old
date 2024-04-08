import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ono_ocr.recognition_worker import recognition_worker


# Create your views here.
def ocr_recognize(request):
    if request.method != "POST":
        return JsonResponse("Method not allowed", status=405)

    try:
        req = json.loads(request.body.decode("utf-8"))
        doctype = req.get("doctype")
        document_path = req.get("document_path")
        data = recognition_worker(document_path, doctype)

        return JsonResponse(
            {
                "message": "Success",
                "doc_path": document_path,
                "doctype": doctype,
                "data": data,
            },
            status=200,
        )
    except Exception as e:
        return JsonResponse(str(e), status=500, safe=False)
