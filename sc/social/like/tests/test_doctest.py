# -*- coding: utf-8 -*-

import unittest
import doctest

from plone.testing import layered

from sc.social.like.testing import FUNCTIONAL_TESTING

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('functional.txt',
                                     optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
        doctest.DocTestSuite(module='sc.social.like'),
    ])
    return suite
