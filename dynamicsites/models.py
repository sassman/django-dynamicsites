# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from .forms import CommaSeparatedSubDomainFormField, FolderNameFormField


"""
Monkey-patch the Site object to include a list of subdomains

Future ideas include:

* Site-enabled checkbox
* Site-groups
* Account subdomains (ala basecamp)
"""


class SubdomainListField(models.TextField):
    description = _("Comma-separated Subdomains")

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CommaSeparatedSubDomainFormField,
            'error_messages': {
                'invalid': _('Enter only subdomains separated by commas.'),
            }
        }
        defaults.update(kwargs)
        return super(SubdomainListField, self).formfield(**defaults)


class FolderNameField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs[
            'help_text'] = _('Folder name for this site\'s files.'
                             'The name may only consist of lowercase characters,'
                             'numbers (0-9), and/or underscores')
        kwargs['max_length'] = 64
        super(FolderNameField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': FolderNameFormField}
        defaults.update(kwargs)
        return super(FolderNameField, self).formfield(**defaults)


# not sure which is better...
# Site.add_to_class('subdomains', SubdomainListField(blank=True))
FolderNameField(blank=True).contribute_to_class(Site, 'folder_name')
SubdomainListField(blank=True).contribute_to_class(Site, 'subdomains')

@property
def has_subdomains(self):
    """
    checks if a Site has subdomains set
    :param self: site instance
    :return:
    """
    return len(self.subdomains) > 0


@property
def default_subdomain(self):
    """
    Return the first subdomain in self.subdomains or '' if no subdomains defined
    """
    if len(self.subdomains):
        return self.subdomains[0]
    return ''

Site.has_subdomains = has_subdomains
Site.default_subdomain = default_subdomain
