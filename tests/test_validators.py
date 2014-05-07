# -*- coding: utf-8 -*-

"""
test_django-dynamicsites
------------

Tests for `django-dynamicsites` validators module.
"""

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase

from dynamicsites.validators import SubDomainValidator


class TestSubDomainValidator(TestCase):

    def test_call(self):
        validator = SubDomainValidator()
        self.assertTrue(callable(validator))
        with self.assertRaises(ValidationError):
            validator('!"§"$%&  "§$')
        with self.assertRaises(ValidationError):
            validator('!"§"$%&')
        with self.assertRaises(ValidationError):
            validator('foo bar')
        with self.assertRaises(ValidationError):
            validator('*')
        validator('foo-bar')
        validator('foo')