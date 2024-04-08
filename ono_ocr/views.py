from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def ocr_recognize(request):
    # Your code here
    
    return HttpResponse("Hello, World! from the recognize function in the views.py file.")
