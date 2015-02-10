# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer

import os.path


def load_image(width, height, format='PNG'):
    filename = os.path.join(
        os.path.dirname(__file__),
        'tests', 'images', 'imgtest_{0}x{1}.{2}'.format(width, height, format.lower()))
    with open(filename, 'rb') as f:
        return f.read()


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import sc.social.like
        self.loadZCML(package=sc.social.like)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'sc.social.like:default')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.social.like:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.social.like:Functional',
)
