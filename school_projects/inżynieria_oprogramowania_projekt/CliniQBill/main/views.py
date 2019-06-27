from django.shortcuts import render
import sys, os
sys.path.insert(0, os.path.abspath('main\library'))
from .library import sqlManager

def home(response):
    resp = sqlManager.dbManagement.getInfoFromdb(sqlManager.dbManagement)
    vars_to_pass = {"resp":resp}
    return render(response, "main/home.html", vars_to_pass)
