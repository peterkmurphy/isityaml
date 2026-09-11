from django.urls import path

from isityaml.views import index as viewindex

app_name = "isityaml"

urlpatterns = [
    path("", viewindex, name="index"),
]
