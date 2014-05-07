# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site


def current_site(request):
    """
    set the current confiugred site to template context
    :param request: request object
    :return: dict with the site set to current site basing on SITE_ID
    """
    return (settings.SITE_ID) and {'site': Site.objects.get_current()} or {}
