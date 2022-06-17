from django.shortcuts import render, HttpResponse
from .models import *

def index(request):
    context = {}
    return render(request, 'drzData/index.html', context)

def contact(request):
    return render(request, 'drzData/contact.html', {})
