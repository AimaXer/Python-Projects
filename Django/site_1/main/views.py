from django.shortcuts import render
from django.http import HttpResponse
import os.path
from .models import ToDoList, Item

def getHtml():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\html_v1.txt"
    f = open(file_path, 'r', encoding = 'UTF-8') 
    html_v2_string = f.read()
    f.close()
    return html_v2_string

def v1(response, name):
    ls = ToDoList.objects.get(name=name)
    items = ls.item_set.get(id=1)
    return HttpResponse("<h1>%s</h1></br><p>%s</p>" %(ls.name, str(items.text)))

def v2(response):
    return HttpResponse(getHtml())