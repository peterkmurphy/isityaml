# Is it YAML?

## About

"Is it YAML?" is a Django application (with tags) for checking whether text is
[YAML](https://yaml.org/) - "a human friendly data serialization
standard for all programming languages" - or not.

Users type or paste text, then click the "Submit" button. If valid YAML has been
entered, the input is shown in
[canonical form](https://yaml.org/spec/1.2.2/#canonical-form); otherwise, the
application presents an error message.

## Installation and Dependencies

"Is it YAML?" depends on [Django](https://www.djangoproject.com/) (≥ 5.2) and
[PyYAML](https://pyyaml.org/) (≥ 6.0). Installation is as simple as:

```bash
pip install isityaml
```

### Setting up

Once installed, add `"isityaml"` to your `INSTALLED_APPS` list in `settings.py`,
and include the app URLs under **any** path prefix you like:

```python
# project urls.py
from django.urls import include, path

urlpatterns = [
    # ... existing routes ...
    path("this_is_the_path_to_isityaml/", include("isityaml.urls")),
]
```

### Creating your own YAML checker page

A YAML checker can be as simple as this Django template file:

```django
{% extends "base.html" %}
{% load isityaml_tags %}
{% block main %}
{% isityaml_checker %}
{% endblock %}
```

Then you can visit the URL where you mounted the app, such as
`/this_is_the_path_to_isityaml/`. Paste or type YAML into the text area and
click **Submit**. Valid input is shown in canonical form; invalid input shows
the parser error and the original text.

### Embedding in another template

Alternately, you can add this to any page with CSRF support:

```django
{% load isityaml_tags %}
{% isityaml_checker %}
```

By default, the form’s `action` is `{% url "isityaml:index" %}`, which resolves
to the `"this_is_the_path_to_isityaml/"` which you included with `isityaml.urls`.
After submission, the user lands on a checker page with the results. To post
somewhere else, you can pass an override:

```django
{% isityaml_checker action_url="/tools/yaml-check/" %}
```

### Text customisation

There are a lot of user interface strings, such as headings, labels and button
text, which live in `isityaml.copy.DEFAULT_COPY`. You can change them in your
settings:

```python
# settings.py
ISITYAML_COPY = {
    "textarea_default": "Xin chào thế giới!", # Hello world! in Vietnamese
    # ...
}
```

Or you can provide them as arguments on the tag:

```django
{% isityaml_checker textarea_default="Xin chào thế giới!" %}
```

### Calling the app from Python

You can even call the application using `isityaml.yaml_check`:

```python
from isityaml.yaml_check import check_yaml, STATE_POST_YES, STATE_POST_NO

result = check_yaml("foo: bar")
if result.yamlstate == STATE_POST_YES:
    print(result.yamlcanon)   # canonical YAML
elif result.yamlstate == STATE_POST_NO:
    print(result.yamlerror)
    print(result.yamloriginal)
```

## Testing

From the package root (with the package importable, e.g. after
`pip install -e .`):

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
```

## History

* 0.1 (August 30th 2011) - Create setup script for files.
* 0.2 (April 25th 2013) - Try to make a half-decent PyPI package.
* 0.3 (January 30th 2014) - Updated to be compatible with Django 1.6 and Mezzanine 3.0.
* 0.4 (February 15th 2014) - Added more error handling and styling to be compatible with Bootstrap.
* 0.5 (August 13th 2014) - Cleaned up error handling and installation issues.
* 0.6 (February 28th 2017) - Updated to be compatible with Django 1.10.
* 0.7 (December 6th 2020) - Run through 2to3 for Python 3 changes.
* 0.8 (September 11th 2026) - Modularise the code; clean up the changes.

## Copyright

The **isityaml** app is copyright (c) 2009-2026
[Peter Murphy](http://www.pkmurphy.com.au/)
<peterkmurphy@gmail.com>.
