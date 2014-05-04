#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import dynamicsites

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = dynamicsites.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-dynamicsites',
    version=version,
    description="""Host multiple sites from a single django project""",
    long_description=readme + '\n\n' + history,
    author='Sven Aßmann',
    author_email='sven.assmann@lubico.biz',
    url='https://github.com/lubico-business/django-dynamicsites',
    packages=[
        'dynamicsites',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-dynamicsites',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)