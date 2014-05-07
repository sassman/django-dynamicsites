# -*- coding: utf-8 -*-
from django.contrib.admin.widgets import AdminTextareaWidget, AdminTextInputWidget


class SubdomainTextarea(AdminTextareaWidget):
    """
    widget to render the Subdomain list
    """

    def render(self, name, value, attrs=None):
        if isinstance(value, (list, tuple, set)):
            value = u', '.join(value)
        return super(SubdomainTextarea, self).render(name, value, attrs)


class FolderNameInput(AdminTextInputWidget):
    class Media:
        js = ['js/dynamicsites/admin.js']

