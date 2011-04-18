import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import sc.social.like

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml',
                     sc.social.like)
    fiveconfigure.debug_mode = False
    ztc.installPackage('sc.social.like')

setup_product()

ptc.setupPloneSite(extension_profiles=['sc.social.like:default'])

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):

        @classmethod
        def tearDown(cls):
            pass



def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='sc.social.like',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='sc.social.like.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        ztc.FunctionalDocFileSuite(
            'browser.txt', 
            package='sc.social.like.docs',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | 
                        doctest.ELLIPSIS,
            test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
