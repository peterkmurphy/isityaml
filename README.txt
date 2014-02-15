===========
Is it YAML?
===========

About
-----

"Is it YAML?" is a Django application for checking whether text is 
`YAML <http://www.yaml.org/>`_ ("a human friendly data serialization
standard for all programming languages"), or not. Users type and/or copy
and paste text and clicks the "Submit" button above. If valid YAML has been
entered, the input is presented in `canonical form <http://www.yaml.org/spec/1.2/spec.html#id2764652>`_.
If not, the application presents an error message.

YAML is just a text format for exchanging data. It exists for cases where 
`XML <http://www.w3.org/XML/>`_ is too much overhead. I like YAML. I find it
more robust in practice than XML (where one missing angle bracket could corrupt
a whole file), yet easier to type by hand.

I conjured up "Is it YAML?" while writing a specification for 
`YPath <https://github.com/peterkmurphy/YPath-Specification>`_ - a language for
addressing parts of a YAML document, as `XPath <http://www.w3.org/TR/xpath/>`_ 
does for XML. To do a proper job of things, I had to write YAML example files.
However, I sometimes needed to check if the example files are good and proper.
"Is it YAML?" gave me a test bed where I can copy-and-paste my examples,
and see if they really are YAML.

Installation and Dependencies
-----------------------------

Apart from `Django <https://www.djangoproject.com/>`_, the app depends on
`PyYAML <https://bitbucket.org/xi/pyyaml>`_, a Python parser for YAML. You
can get the application from PyPI through the command::

    pip install isityaml

Once installed, just add "isityaml" to your INSTALLED_APPS list in settings.py,
and add the desired URL in one of the urls.py files.

The HTML template file used to generate HTML has been redesigned to work with the 
`Mezzanine <http://mezzanine.jupo.org/>`_ CMS. The redesign removed any explicit
references to particular stylesheets found with earlier versions. Feel free to
customise: the app is released under a 3 clause BSD license. See LICENSE.txt for 
more information. If you wish to do any changes, pop over to the `GitHub repository 
<https://github.com/peterkmurphy/isityaml>`_ for the app. 

History
-------


* 0.1 (August 30th 2011) - Create setup script for files.

* 0.2 (April 25th 2013) - Try to make a half-decent PyPI package.

* 0.3 (January 30th 2014) - Updated to be compatible with Django 1.6 and Mezzanine 3.0.

* 0.4 (February 15th 2014) - Added more error handling and styling to be compatible with Bootstrap.

Copyright
---------

The **isityaml** app is copyright (c) 2008-2014 
`Peter Murphy <http://www.pkmurphy.com.au/>`_ 
<peterkmurphy@gmail.com>.




