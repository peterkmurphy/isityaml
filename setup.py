#!/usr/bin/env python

from distutils.core import setup
#from setuptools import setup

setup(name='isityaml',
    version='0.4.7',
    description='A Django app for checking the correctness of YAML',
    author='Peter Murphy',
    author_email='peterkmurphy@gmail.com',
    url='http://pypi.python.org/pypi/isityaml/',
    packages=['isityaml'],
    package_data={
        'isityaml': [
            'templates/isityaml/*.html',
        ],
    },
    keywords = 'YAML parse text Django',
    license='LICENSE.txt',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        'License :: OSI Approved :: BSD License',        
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',        
        "Topic :: Education",
        ],
    long_description=open('README.rst').read(),
    install_requires = ["Django >= 1.1.1", "mezzanine>=3.0","PyYAML >= 3.0"],
)
