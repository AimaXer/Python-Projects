from django.shortcuts import render
from django.http import HttpResponse

def v1(response):
    return HttpResponse("<h1>Samolot</h1>")

with open('html_v1.html', 'r') as f: 
    html_v2_string = f.read()

def v2(response):
    return HttpResponse(html_v2_string)