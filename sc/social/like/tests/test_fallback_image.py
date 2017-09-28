# -*- coding: utf-8 -*-
from sc.social.like.testing import INTEGRATION_TESTING
from sc.social.like.tests.utils import get_file_b64encoded
from sc.social.like.utils import validate_og_fallback_image
from zope.interface import Invalid

import unittest


class OGFallbackImageValidatorTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_validate_og_fallback_image_no_image(self):
        self.assertTrue(validate_og_fallback_image(None))

    def test_validate_og_fallback_image_valid(self):
        image = get_file_b64encoded('imgtest_1024x768.png')
        self.assertTrue(validate_og_fallback_image(image))

    def test_validate_og_fallback_image_invalid_mime_type(self):
        image = get_file_b64encoded('julia_set_ice.tiff')
        with self.assertRaises(Invalid):
            validate_og_fallback_image(image)

    # FIXME: we need to find out how to easily resize the image
    @unittest.expectedFailure
    def test_validate_og_fallback_image_invalid_size(self):
        image = get_file_b64encoded('imgtest_1024x768.png')
        with self.assertRaises(Invalid):
            validate_og_fallback_image(image)

    def test_validate_og_fallback_image_invalid_dimensions(self):
        image = get_file_b64encoded('julia_set_ice.png')
        with self.assertRaises(Invalid):
            validate_og_fallback_image(image)

    def test_validate_og_fallback_image_invalid_aspect_ratio(self):
        image = get_file_b64encoded('imgtest_768x768.jpg')
        with self.assertRaises(Invalid):
            validate_og_fallback_image(image)
