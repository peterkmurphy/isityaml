"""Views for the Is it YAML? checker page."""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from isityaml.yaml_check import check_yaml, empty_check_result


@csrf_protect
def index(request):
    """Render the checker page; on POST, validate submitted YAML text."""
    if request.method == "POST":
        result = check_yaml(request.POST.get("yamlarea"))
    else:
        result = empty_check_result()
    return render(request, "isityaml/isityaml.html", result.as_context())
