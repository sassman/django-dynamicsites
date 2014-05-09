# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase, RequestFactory, Client
from django.test.utils import override_settings

from dynamicsites.views import site_info


class TestSiteInfoView(TestCase):
    def setUp(self):
        super(TestSiteInfoView, self).setUp()
        self.factory = RequestFactory()

    def test_not_get(self):
        f = self.factory
        methods = [
            f.post,
            f.delete,
            f.put,
            f.patch,
            f.head
        ]
        view = site_info
        for method in methods:
            request = method('/site-info')
            with self.assertRaises(Http404):
                view(request)

    def test_get_successfully(self):
        http_host = 'www.example.com'
        c = Client(HTTP_HOST=http_host)
        response = c.get(reverse('site_info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, http_host)

    @override_settings(SITE_ID=2)
    def test_get_other_site_sucessfully(self):
        Site.objects.get_or_create(
            domain='starfleet.com',
            subdomains='www,ships',
            folder_name='a',
            id=2
        )

        http_host = 'www.starfleet.com'
        c = Client(HTTP_HOST=http_host)
        response = c.get(reverse('site_info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, http_host)
