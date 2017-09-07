# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from sc.social.like.utils import get_content_image
from sc.social.like.utils import validate_canonical_domain
from sc.social.like.utils import validate_description_social
from sc.social.like.utils import validate_image_social
from sc.social.like.utils import validate_title_social
from zope.interface import Invalid

import unittest


class UtilsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(
                self.portal, type='News Item', id='foo')
            set_image_field(self.obj, load_image(1024, 768), 'image/png')

            self.obj2 = api.content.create(
                self.portal, type='News Item', id='foo2')
            set_image_field(self.obj2, load_image(200, 200), 'image/png')

            self.obj3 = api.content.create(
                self.portal, type='News Item', id='foo3')
            set_image_field(self.obj3, load_image(200, 200), 'image/bmp')

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

    def test_validate_title_social_valid(self):
        self.assertFalse(validate_title_social('Lorem ipsum dolor sit amet, '
                                               'consectetur adipiscing elit.'))

    def test_validate_title_social_invalid(self):
        self.assertTrue(validate_title_social('Integer molestie massa auctor diam '
                                              'volutpat, et sodales lectus pulvinar.'))

    def test_validate_description_social_valid(self):
        self.assertFalse(validate_title_social('Lorem ipsum dolor sit amet, '
                                               'consectetur adipiscing elit.'))

    def test_validate_description_social_invalid(self):
        self.assertTrue(validate_description_social('Integer molestie massa auctor diam '
                                                    'volutpat, et sodales lectus pulvinar.'))

        self.assertTrue(validate_description_social('Sed pellentesque quam tincidunt neque imperdiet porta. '
                                                    'Fusce nec vestibulum felis, ut faucibus odio. Maecenas sit '
                                                    'amet dapibus diam.'))

    def test_validate_image_social_valid(self):
        image = get_content_image(self.obj)
        self.assertFalse(validate_image_social(image))

    def test_validate_image_social_invalid(self):
        image = get_content_image(self.obj2)
        self.assertTrue(validate_image_social(image))
        image = get_content_image(self.obj3)
        self.assertTrue(validate_image_social(image))
