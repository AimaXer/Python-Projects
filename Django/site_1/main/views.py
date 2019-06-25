from django.shortcuts import render
from django.http import HttpResponse
import os.path
from .models import ToDoList, Item

def home(request):
    return render(request, 'index.html')