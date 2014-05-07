# -*- coding: utf-8 -*-
import re
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import SubdomainTextarea, FolderNameInput
from .validators import SubDomainValidator


logger = logging.getLogger(__name__)


class CommaSeparatedSubDomainFormField(forms.Field):
    """
    A form field to accept a string of subdomains, separated by commas
    If blank or an asterisk '*', allow all subdomains
    """
    description = _("Comma-separated sub domains")

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = SubdomainTextarea()
        super(CommaSeparatedSubDomainFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """

        return list of sub domains. splitting string by \n \r or ','
        """
        if not value:
            value = ''

        if not isinstance(value, (list, tuple, set)):
            # strip whitespaces
            value = re.sub(' ', '', str(value))
            # split by
            value = re.split('\n|\r|,', value)
            list_value = [v for v in value if v is not '*' and v]
        else:
            list_value = list(value)

        return list_value

    def validate(self, value):
        """
        Uses SubDomainValidator to validate a list of sub domains

        :param value: list of sub domains
        :type value: list tuple set str
        """
        value = self.to_python(value)
        super(CommaSeparatedSubDomainFormField, self).validate(value)

        validate = SubDomainValidator()
        for subdomain in value:
            validate(subdomain)


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
        if value:
            value = value.strip().lower()
        return value

    def validate(self, value):
        """
        Validates the folder name is a valid Python package name
        Verifies if the folder name exists by trying to
        do an import
        """
        valid = super(FolderNameFormField, self).validate(value)
        if not value or not valid or re.search(r"[^a-z0-9_]", value):
            raise ValidationError('The folder name must only contain letters, numbers, or underscores')
        try:
            __import__("sites.{0}".format(value))
        except ImportError:
            raise ValidationError(
                'The folder sites/{0}/ does not exist or is missing the __init__.py file'.format(value)
            )