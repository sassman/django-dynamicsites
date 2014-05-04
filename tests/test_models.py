# -*- coding: utf-8 -*-

"""
test_django-dynamicsites
------------

Tests for `django-dynamicsites` models module.
"""

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.test.testcases import TestCase
from django.utils import unittest
from dynamicsites.forms import SubdomainListFormField, FolderNameFormField


class TestSiteModel(TestCase):
    def test_extended_fields(self):
        folder_name = 'about_food_com'
        subdomains=['www', 'fruta', 'carne', 'legumes', 'leite']
        site, created = Site.objects.get_or_create(
            domain='about-food.com',
            name='Site About Food',
            folder_name=folder_name,
            subdomains=subdomains
        )
        self.assertTrue(created)
        self.assertEqual(site.folder_name, folder_name)
        self.assertEqual(site.subdomains, subdomains)

        self.assertTrue(site.has_subdomains)
        self.assertEqual(site.default_subdomain, subdomains[0])

    def test_empty_subdomain(self):
        folder_name = 'google_com'
        subdomains = []
        site, created = Site.objects.get_or_create(
            domain='google.com',
            name='Google',
            folder_name=folder_name,
            subdomains=subdomains
        )
        self.assertTrue(created)
        self.assertFalse(site.has_subdomains)
        self.assertEqual(site.default_subdomain, '')

    @unittest.skip('TODO fix this stupid cleanup to an empty list')
    def test_empty_subdomain_strings_in_list(self):
        folder_name = 'google_com'
        subdomains = ['', '', '']
        site, created = Site.objects.get_or_create(
            domain='google.com',
            name='Google',
            folder_name=folder_name,
            subdomains=subdomains
        )
        self.assertTrue(created)
        # TODO this is stupid, better cleanup to an empty list
        self.assertFalse(site.has_subdomains, site.subdomains)
        self.assertEqual(site.default_subdomain, '')

    @unittest.skip('TODO fix that this test works, not allow to store such crap')
    def test_empty_subdomain_strings_in_string(self):
        folder_name = 'google_com'
        # TODO fix that this test works, not allow to store such crap
        subdomains = '"", "", ""'
        with self.assertRaises(ValidationError):
            site, created = Site.objects.get_or_create(
                domain='google.com',
                name='Google',
                folder_name=folder_name,
                subdomains=subdomains
            )

    def test_formfield_from_model(self):
        class SiteForm(ModelForm):
            class Meta:
                model = Site
        site_form = SiteForm()
        formfield = site_form.fields['subdomains']
        self.assertEqual(type(formfield), SubdomainListFormField)

        formfield = site_form.fields['folder_name']
        self.assertEqual(type(formfield), FolderNameFormField)
