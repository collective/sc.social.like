# -*- coding: utf-8 -*-
from plone.testing import layered
from sc.social.like.config import IS_PLONE_5
from sc.social.like.testing import ROBOT_TESTING

import os
import robotsuite
import unittest


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith('test_') and f.endswith('.robot')]

# FIXME: skip RobotFramework tests in Plone 5
if IS_PLONE_5:
    tests = []


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            robotsuite.RobotTestSuite(t, noncritical=['Expected Failure']),
            layer=ROBOT_TESTING)
        for t in tests
    ])
    return suite
