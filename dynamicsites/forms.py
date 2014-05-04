# -*- coding: utf-8 -*-
import re
import logging

from django import forms
from django.core.validators import URLValidator, ValidationError, RegexValidator
from .widgets import SubdomainTextarea, FolderNameInput


logger = logging.getLogger(__name__)


class SubdomainListFormField(forms.Field):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = SubdomainTextarea()
        super(SubdomainListFormField, self).__init__(*args, **kwargs)

    """
    A form field to accept a string of subdomains, separated by commas
    If blank or an asterisk '*', allow all subdomains
    """

    def to_python(self, value):
        """
        return list of subdomains
        """
        if not value:
            return []

        # convert newlines to commas
        value = re.sub("\n|\r", ',', value)

        # clean incoming subdomains
        subdomains = []
        for subdomain in value.split(','):
            subdomain = subdomain.strip().lower()
            if subdomain and subdomain is not '*':
                subdomains.append(subdomain)
        return subdomains

    def validate(self, value):
        """
        Uses URLValidator to validate subdomains
        """
        # TODO Make a SubdomainValidator as a subclass of
        # URLValidator and use it both in model and form fields (ala URLField)
        super(SubdomainListFormField, self).validate(value)

        u = URLValidator()
        for subdomain in value:
            logger.debug('validating %s', subdomain)
            if subdomain == "''":
                logger.debug('passing')
                pass
            else:
                test_host = 'http://%s.example.com/' % subdomain
                logger.debug('testing %s', test_host)
                u(test_host)


class FolderNameFormField(forms.CharField):
    """
    A form field to accept a foldername for this site
    """

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = FolderNameInput()
        super(FolderNameFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        return value stripped of leading/trailing whitespace, and lowercased
        """
        return value.strip().lower()

    def validate(self, value):
        """
        Validates the folder name is a valid Python package name
        Verifies if the folder name exists by trying to
        do an import
        """
        super(FolderNameFormField, self).validate(value)

        if re.search(r"[^a-z0-9_]", value):
            raise ValidationError('The folder name must only contain letters, numbers, or underscores')
        try:
            __import__("sites.%s" % value)
        except ImportError:
            raise ValidationError('The folder sites/%s/ does not exist or is missing the __init__.py file' % value)