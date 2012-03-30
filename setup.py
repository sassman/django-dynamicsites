import os
import sys
from distutils.core import setup

version = __import__('dynamicsites').get_version()

setup(
    name='dynamicsites',
    version=version,
    description="Host multiple sites from a single django project",
    url='https://bitbucket.org/uysrc/django-dynamicsites',
    platforms=['any'],
    packages=['dynamicsites'],
)
