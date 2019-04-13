from django.shortcuts import render
from django.http import HttpResponse
import os.path

def getHtml():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "\\html_v1.txt"
    f = open(file_path, 'r', encoding = 'UTF-8') 
    html_v2_string = f.read()
    f.close()
    return html_v2_string

def v1(response):
    return HttpResponse("<h1>Samolot</h1>")

def v2(response):
    return HttpResponse(getHtml())