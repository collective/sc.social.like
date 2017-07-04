# -*- coding: utf-8 -*-
from sc.social.like.utils import validate_canonical_domain
from zope.interface import Invalid

import unittest


class UtilsTestCase(unittest.TestCase):

    def test_validate_canonical_domain_valid(self):
        self.assertTrue(validate_canonical_domain('http://example.org'))
        self.assertTrue(validate_canonical_domain('https://example.org'))

    def test_validate_canonical_domain_invalid(self):
        with self.assertRaises(Invalid):
            validate_canonical_domain('https://example.org/foo?bar')
        with self.assertRaises(Invalid):
            validate_canonical_domain('http://example.org/')  # path
        with self.assertRaises(Invalid):
            validate_canonical_domain('https://example.org?foo')  # query
        with self.assertRaises(Invalid):
            validate_canonical_domain('https://example.org#bar')  # fragment
