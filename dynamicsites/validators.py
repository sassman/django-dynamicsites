# -*- coding: utf-8 -*-
from django.core.validators import URLValidator


class SubDomainValidator(URLValidator):
    format_string = 'https://{0}.domain.com'

    def __call__(self, value):
        value = self.format_string.format(value)
        return super(SubDomainValidator, self).__call__(value)