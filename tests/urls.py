# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^site-info/$', 'dynamicsites.views.site_info', name='site_info'),
)