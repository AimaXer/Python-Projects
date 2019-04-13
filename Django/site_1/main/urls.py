from django.urls import path
from . import views

urlpatterns = [
    path("<str:name>", views.v1, name="v1"),
    path("v2/", views.v2, name="v2"),
]