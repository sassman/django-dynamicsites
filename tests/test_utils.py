# -*- coding: utf-8 -*-
import threading
from django.test import TestCase
from dynamicsites.utils import make_tls_property


class TestTLSProperty(TestCase):

    class Borg(object):
        COLLECTIVE = 'shared'

    def borg(self):
        return TestTLSProperty.Borg()

    def test_creation(self):
        borg = self.borg()
        self.assertEqual(borg.COLLECTIVE, 'shared')
        TestTLSProperty.Borg.YOU = 'picard'
        self.assertEqual(TestTLSProperty.Borg.YOU, 'picard')
        borg.YOU = make_tls_property(borg.COLLECTIVE)
        self.assertEqual(borg.COLLECTIVE, 'shared')
        self.assertEqual(borg.YOU.value, 'shared')
        borg.COLLECTIVE = 'we arg borg'
        self.assertEqual(borg.YOU.value, 'shared')
        self.assertEqual(borg.YOU.value, 'shared')
        borg.YOU.value = 'seven of nine'
        self.assertEqual(borg.YOU.value, 'seven of nine')

    def test_value_manipulation(self):
        borg = self.borg()
        borg.YOU = make_tls_property(borg.COLLECTIVE)
        borg.YOU.value = 'seven of nine'
        self.assertEqual(borg.YOU.value, 'seven of nine')

        def individual_mind():
            borg.YOU.value = 'borg queen'
            self.assertEqual(borg.YOU.value, 'borg queen')

        thread = threading.Thread()
        thread.run = individual_mind
        thread.start()
        thread.join(60)

        self.assertEqual(borg.YOU.value, 'seven of nine')