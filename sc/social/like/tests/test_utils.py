# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.testing import load_image
from sc.social.like.tests.api_hacks import set_image_field
from sc.social.like.tests.utils import get_random_string
from sc.social.like.utils import get_content_image
from sc.social.like.utils import validate_canonical_domain
from sc.social.like.utils import validate_og_description
from sc.social.like.utils import validate_og_lead_image
from sc.social.like.utils import validate_og_title
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


class OGValidatorsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(
                self.portal, 'News Item', title='Lorem ipsum')
        set_image_field(self.obj, load_image(1024, 768), 'image/png')

    def test_validate_og_title_valid(self):
        self.assertTrue(validate_og_title('foo'))

    def test_validate_og_title_invalid(self):
        from sc.social.like.config import OG_TITLE_MAX_LENGTH
        from sc.social.like.utils import MSG_INVALID_OG_TITLE

        with self.assertRaises(ValueError):
            validate_og_title(None)
        with self.assertRaises(ValueError):
            validate_og_title('')

        title = get_random_string(OG_TITLE_MAX_LENGTH + 1)
        with self.assertRaises(ValueError):
            validate_og_title(title)

        # test validation message
        try:
            validate_og_description(title)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_TITLE)

    def test_validate_og_description_valid(self):
        self.assertTrue(validate_og_description(None))
        self.assertTrue(validate_og_description(''))
        self.assertTrue(validate_og_description('foo'))

    def test_validate_og_description_invalid(self):
        from sc.social.like.config import OG_DESCRIPTION_MAX_LENGTH
        from sc.social.like.utils import MSG_INVALID_OG_DESCRIPTION

        description = get_random_string(OG_DESCRIPTION_MAX_LENGTH + 1)
        with self.assertRaises(ValueError):
            validate_og_description(description)

        # test validation message
        try:
            validate_og_description(description)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_DESCRIPTION)

    def test_validate_og_lead_image_no_image(self):
        self.assertTrue(validate_og_lead_image(None))

    def test_validate_og_lead_image_valid(self):
        image = get_content_image(self.obj)
        self.assertTrue(validate_og_lead_image(image))

    def test_validate_og_lead_image_invalid_mime_type(self):
        from sc.social.like.utils import MSG_INVALID_OG_LEAD_IMAGE_MIME_TYPE

        image = get_content_image(self.obj)
        # HACK: change image MIME type to test the validator
        image.mimetype = 'image/tiff'
        with self.assertRaises(ValueError):
            validate_og_lead_image(image)

        # test validation message
        try:
            validate_og_lead_image(image)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_LEAD_IMAGE_MIME_TYPE)

    def test_validate_og_lead_image_invalid_size(self):
        from sc.social.like.config import OG_LEAD_IMAGE_MAX_SIZE
        from sc.social.like.utils import MSG_INVALID_OG_LEAD_IMAGE_SIZE

        image = get_content_image(self.obj)
        # HACK: change image scale data to test the validator
        image.data.data = get_random_string(OG_LEAD_IMAGE_MAX_SIZE + 1)
        with self.assertRaises(ValueError):
            validate_og_lead_image(image)

        # test validation message
        try:
            validate_og_lead_image(image)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_LEAD_IMAGE_SIZE)

    def test_validate_og_lead_image_invalid_dimensions(self):
        from sc.social.like.utils import MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS

        # HACK: change image scale to test the validator
        image = get_content_image(self.obj, scale='preview')
        with self.assertRaises(ValueError):
            validate_og_lead_image(image)

        # test validation message
        try:
            validate_og_lead_image(image)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)

    def test_validate_og_lead_image_invalid_aspect_ratio(self):
        from sc.social.like.utils import MSG_INVALID_OG_LEAD_IMAGE_ASPECT_RATIO

        set_image_field(self.obj, load_image(768, 768, 'JPG'), 'image/jpeg')
        image = get_content_image(self.obj)
        with self.assertRaises(ValueError):
            validate_og_lead_image(image)

        # test validation message
        try:
            validate_og_lead_image(image)
        except ValueError as e:
            self.assertEqual(str(e), MSG_INVALID_OG_LEAD_IMAGE_ASPECT_RATIO)


def load_tests(loader, tests, pattern):
    from sc.social.like.testing import HAS_DEXTERITY

    test_cases = [UtilsTestCase]
    if HAS_DEXTERITY:
        # load validation tests on Dexterity-based content types only
        test_cases.append(OGValidatorsTestCase)

    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
