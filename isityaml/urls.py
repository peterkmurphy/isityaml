# Deprecated and removed in Django 1.6:
# Deprecated and removed in Django 1.6:
from django.conf.urls import url, include
from isityaml.views import index as viewindex

urlpatterns =[ url(r'^$', viewindex)]
