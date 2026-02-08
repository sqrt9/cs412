from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.

context = {}

def base(request : HttpRequest):
    return render(request, "testpages/base.html", context)
    
