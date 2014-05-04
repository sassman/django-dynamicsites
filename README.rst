=============================
django-dynamicsites
=============================

.. image:: https://badge.fury.io/py/django-dynamicsites.png
    :target: https://badge.fury.io/py/django-dynamicsites

.. image:: https://travis-ci.org/lubico-business/django-dynamicsites.svg?branch=feature/pypi-cleanup
    :target: https://travis-ci.org/lubico-business/django-dynamicsites

.. image:: https://coveralls.io/repos/sassman/django-dynamicsites/badge.png
    :target: https://coveralls.io/r/lubico-business/django-dynamicsites

Host multiple sites from a single django project.

Using django-dynamicsites you can host multiple sites within a single
domain in terms of vhost configuration. This may be the most common setup to allow different url mappings by subdomain.

Expands the standard ``django.contrib.sites`` package to allow for:

 * Sites identified dynamically from the request via middleware
 * No need for multiple virtual hosts at the webserver level
 * 301 Redirects to canonical hostnames
 * Allows for a site to support multiple subdomains
 * Allows for a site to be an independent subdomain of another site
 * A site may have its own urls.py and templates
 * A single site may accept requests from multiple hostnames
 * Allows for environment hostname mappings to use non-production hostnames (for use in dev, staging, test, etc. environments)

Credits
-------

Original code is derived from UYSRC <http://www.uysrc.com/> and come from https://bitbucket.org/uysrc/django-dynamicsites
More info can be found here: http://blog.uysrc.com/2011/03/23/serving-multiple-sites-with-django/

Documentation
-------------

The full documentation is at https://django-dynamicsites.readthedocs.org.

Quickstart
----------

Install django-dynamicsites::

    pip install django-dynamicsites
