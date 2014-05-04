# -*- coding: utf-8 -*-
import re
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


comma_separated_slug_list_re = re.compile('^[\w,]*$')
validate_comma_separated_slug_list = RegexValidator(comma_separated_slug_list_re, _('Enter only strings separated '
                                                                                    'by commas.'), 'invalid')
