# -*- coding: utf-8 -*-

"""
test_django-dynamicsites
------------

Tests for `django-dynamicsites` forms module.
"""
import sys

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test.testcases import TestCase
from django.utils import unittest
from dynamicsites.forms import CommaSeparatedSubDomainFormField, FolderNameFormField
from dynamicsites.widgets import SubdomainTextarea, FolderNameInput


class TestCommaSeparatedSubDomainFormField(TestCase):

    def field(self):
        return CommaSeparatedSubDomainFormField()

    def test_defaults(self):
        field = self.field()
        self.assertEqual(type(field.widget), SubdomainTextarea)

    def test_to_python(self):
        field = self.field()
        self.assertEqual(field.to_python(None), [])
        list_value = ['a', 'b']
        self.assertEqual(field.to_python(list_value), list_value)
        set_value = ('a', 'b')
        self.assertEqual(field.to_python(set_value), list_value)
        tuple_value = {'a', 'b'}
        self.assertListEqual(sorted(field.to_python(tuple_value)), list_value)
        string_value = 'a, b,,'
        self.assertEqual(field.to_python(string_value), list_value)
        string_value = 'a,                      b'
        self.assertEqual(field.to_python(string_value), list_value)
        string_value = """a
                          b"""
        self.assertEqual(field.to_python(string_value), list_value)
        string_value = """a\n\n\n\n\n
                          \rb"""
        self.assertEqual(field.to_python(string_value), list_value)
        string_value = u"""a\n\n\n\n\n
                            \rb"""
        self.assertEqual(field.to_python(string_value), list_value)

    def test_validate(self):
        field = self.field()
        list_value = ['a', 'b']
        self.assertNotEquals(field.validate(list_value), True)
        list_value = ['a*!"§$%', 'b-hello-worlds*!"§']
        with self.assertRaises(ValidationError):
            field.validate(list_value)
        string_value = 'a*!"§$%, b-hello-worlds*!"§'
        with self.assertRaises(ValidationError):
            field.validate(string_value)
        string_value = u'a, b'
        field.validate(string_value)


class TestFolderNameField(TestCase):
    def field(self):
        return FolderNameFormField()

    def test_defaults(self):
        field = self.field()
        self.assertEqual(type(field.widget), FolderNameInput)

    def test_to_python(self):
        field = self.field()
        self.assertEqual(field.to_python(None), None)
        self.assertEqual(field.to_python('abc'), 'abc')
        self.assertEqual(field.to_python('aBc'), 'abc')
        self.assertEqual(field.to_python('ABC'), 'abc')
        self.assertEqual(field.to_python('A!C'), 'a!c')
        self.assertEqual(field.to_python('A!C '), 'a!c')
        self.assertEqual(field.to_python(' A!C '), 'a!c')
        self.assertEqual(field.to_python(' A!C'), 'a!c')

    def test_validate_not_exists_site_folder(self):
        field = self.field()
        with self.assertRaises(ValidationError):
            field.validate('b')

    @unittest.skipIf(sys.version_info > (3, 3), 'since that version all dirs are valid '
                                                'packages even without __init__.py')
    def test_validate_invalid_package_site_folder(self):
        field = self.field()
        with self.assertRaises(ValidationError):
            field.validate('d')

    def test_validate_invalid_folder_name(self):
        field = self.field()
        with self.assertRaises(ValidationError):
            field.validate('!"§$%')

    def test_validate_successfully(self):
        field = self.field()
        field.validate('a')
        field.validate('c')


@unittest.skip('TODO rewrite to see only if a ModelForm will utilize fields as expected')
class TestSiteForm(TestCase):

    def setUp(self):
        super(TestSiteForm, self).setUp()
        class SiteForm(ModelForm):
            class Meta:
                model = Site
        self.site_form = SiteForm

    def test_empty_form(self):
        site_form = self.site_form()
        self.assertFalse(site_form.is_valid())

    def test_subdomains_field_with_list_input(self):
        # test if list data is not accepted
        list_data = {'subdomains': ['a', 'b', 'c']}
        site_form = self.site_form(data=list_data)
        self.assertFalse(site_form.is_valid())
        self.assertEqual(site_form.cleaned_data.get('subdomains'), [])

    def test_subdomains_field_with_invalid_string_input(self):
        string_data = {'subdomains': 'a*!?"§, b afasdfa-'}
        with self.assertRaises(ValidationError):
            site_form = self.site_form(data=string_data)
            site_form.is_valid()

    def test_subdomains_field_with_valid_string_input(self):
        string_data = {'subdomains': 'a, b, c'}
        site_form = self.site_form(data=string_data)
        cleaned_data = site_form.clean()
        self.assertEqual(cleaned_data.get('subdomains'), ['a', 'b', 'c'])


