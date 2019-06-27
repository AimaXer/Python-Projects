from django.shortcuts import render
from subprocess import Popen
import os

def home(response):
    resp = Popen('python '+ os.path.abspath('main\library\sqlManager.py')).stdout
    vars_to_pass = {"resp":str(resp)}
    return render(response, "main/home.html", vars_to_pass)
