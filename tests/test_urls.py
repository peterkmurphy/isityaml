"""URLConf used only by isityaml Django tests."""

from django.urls import include, path

urlpatterns = [
    path("", include("isityaml.urls")),
]
