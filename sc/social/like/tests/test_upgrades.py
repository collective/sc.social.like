# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.testing import INTEGRATION_TESTING

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'sc.social.like:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1to2TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3020', u'3030')

    def test_upgrade_to_3030_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 3)

    def test_move_mobile_detection_client_side(self):
        # check if the upgrade step is registered
        title = u'Move mobile detection client-side'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        js_tool = api.portal.get_tool('portal_javascripts')
        JS_ID = '++resource++sl_scripts/social_like.js'

        # simulate state on previous version
        js_tool.unregisterResource(JS_ID)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        # Check
        self.assertIn(JS_ID, js_tool.getResourceIds())
