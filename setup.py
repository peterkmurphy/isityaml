#!/usr/bin/env python

import os
from distutils.core import setup

def fullsplit(path, result=None):
    """
Split a pathname into components (the opposite of os.path.join) in a
platform-neutral way.
"""
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


package_dir = "isityaml"


packages = []
for dirpath, dirnames, filenames in os.walk(package_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
]

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)


setup(name='isityaml',
    version='0.1',
    description='A Django app for checking YAML',
    author='Peter Murphy',
    author_email='peterkmurphy@gmail.com',
    url='http://www.pkmurphy.com.au/isityaml/',
    packages=packages,
    package_data=package_data,
    download_url = "http://www.pkmurphy.com.au/images/packages/isityaml-0.1.tar.gz",
    keywords = ["YAML", "parse", "text", "Django"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        ],
    long_description = """\
        "Is it YAML?" is a test bed where files can be checked if they are YAML."""
)