# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.

Tile for collective.cover is only tested in Plone 4.3.
"""
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import os.path
import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE

try:
    pkg_resources.get_distribution('collective.cover')
except pkg_resources.DistributionNotFound:
    HAS_COVER = False
else:
    HAS_COVER = True


def load_image(width, height, format='PNG'):
    filename = os.path.join(
        os.path.dirname(__file__),
        'tests', 'images', 'imgtest_{0}x{1}.{2}'.format(width, height, format.lower()))
    with open(filename, 'rb') as f:
        return f.read()


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if HAS_COVER:
            import collective.cover
            self.loadZCML(package=collective.cover)

        import sc.social.like
        self.loadZCML(package=sc.social.like)

    def setUpPloneSite(self, portal):
        if HAS_COVER:
            self.applyProfile(portal, 'collective.cover:default')

        self.applyProfile(portal, 'sc.social.like:default')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.social.like:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.social.like:Functional',
)
ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='sc.social.like:Robot',
)
