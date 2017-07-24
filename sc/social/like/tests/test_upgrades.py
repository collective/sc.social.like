# -*- coding: utf-8 -*-
from plone import api
from sc.social.like.config import IS_PLONE_5
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.testing import HAS_DEXTERITY
from sc.social.like.testing import INTEGRATION_TESTING
from zope.component import getUtility

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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


class To3030TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3020', u'3030')

    def test_upgrade_to_3030_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 3)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
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


class To3040TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3030', u'3040')

    def test_upgrade_to_3040_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    def test_update_configlet_information(self):
        # check if the upgrade step is registered
        title = u'Update configlet information'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        controlpanel = api.portal.get_tool(name='portal_controlpanel')
        configlet = controlpanel.getActionObject('Products/sociallikes')
        configlet.setActionExpression('string:${portal_url}/@@likes-providers')
        assert configlet.getActionExpression().endswith('@@likes-providers')

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        configlet = controlpanel.getActionObject('Products/sociallikes')
        self.assertTrue(
            configlet.getActionExpression().endswith('@@sociallike-settings'))

    def test_migrate_settings_to_registry(self):
        # check if the upgrade step is registered
        title = u'Migrate package settings to registry'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from plone.registry.interfaces import IRegistry
        from sc.social.like.config import PROJECTNAME

        # restore old property sheet
        portal_properties = api.portal.get_tool(name='portal_properties')
        portal_properties.manage_addPropertySheet('sc_social_likes_properties')
        old_props = portal_properties['sc_social_likes_properties']
        enabled_portal_types = ('Event', 'Document', 'News Item', 'File')
        old_props.manage_addProperty(
            'enabled_portal_types', enabled_portal_types, 'lines')
        old_props.manage_addProperty('typebutton', 'horizontal', 'string')
        old_props.manage_addProperty('twittvia', '', 'string')
        old_props.manage_addProperty('fbaction', '', 'string')
        old_props.manage_addProperty('fbadmins', '', 'string')
        old_props.manage_addProperty('fbapp_id', '', 'string')
        old_props.manage_addProperty('fbbuttons', ('Like',), 'lines')
        plugins_enabled = ('Facebook', 'Twitter', 'Google+')
        old_props.manage_addProperty(
            'plugins_enabled', plugins_enabled, 'lines')
        old_props.manage_addProperty('do_not_track', False, 'boolean')

        # simulate assignment via form using field type TextLine (unicode)
        # we are now using and ASCIILine field (str)
        old_props.twittvia = u'hvelarde'
        old_props.fbadmins = u'hvelarde'
        old_props.fbapp_id = None  # form had no default values

        # remove registry settings
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool(name='portal_setup')
        setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
        registry = getUtility(IRegistry)
        with self.assertRaises(KeyError):
            registry.forInterface(ISocialLikeSettings)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        self.assertNotIn('sc_social_likes_properties', portal_properties)

        settings = registry.forInterface(ISocialLikeSettings)
        self.assertEqual(settings.enabled_portal_types, enabled_portal_types)
        self.assertEqual(settings.plugins_enabled, plugins_enabled)
        self.assertEqual(settings.typebutton, u'horizontal')
        self.assertFalse(settings.do_not_track)
        self.assertEqual(settings.fbaction, u'like')
        self.assertEqual(settings.facebook_username, 'hvelarde')
        self.assertEqual(settings.facebook_app_id, '')
        self.assertEqual(settings.fbbuttons, (u'Like',))
        self.assertEqual(settings.twitter_username, 'hvelarde')


class To3041TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3040', u'3041')

    def test_upgrade_to_3041_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)

    def test_register_cover_tiles(self):
        # check if the upgrade step is registered
        title = u'Register collective.cover tiles'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from sc.social.like.config import TILES
        registered = api.portal.get_registry_record('plone.app.tiles')
        [registered.remove(t) for t in TILES if t in registered]
        # there are no elements in common
        assert set(registered) & set(TILES) == set([])

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        registered = api.portal.get_registry_record('plone.app.tiles')
        [self.assertIn(t, registered) for t in TILES]


class To3042TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3041', u'3042')

    def test_upgrade_to_3042_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)


class To3043TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3042', u'3043')

    def test_upgrade_to_3043_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)


class To3044TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3043', u'3044')

    def test_upgrade_to_3043_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)

    def test_add_fbshowlikes_record(self):
        title = u'Add registry setting to show/hide number of likes'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from plone.registry.interfaces import IRegistry
        registry = getUtility(IRegistry)
        record = ISocialLikeSettings.__identifier__ + '.fbshowlikes'
        del registry.records[record]
        assert record not in registry

        with self.assertRaises(KeyError):
            registry.forInterface(ISocialLikeSettings)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        # Test if our setting is there and set
        settings = registry.forInterface(ISocialLikeSettings)
        self.assertEqual(settings.fbshowlikes, True)


class To3045TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3044', u'3045')

    def test_upgrade_to_3045_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    def test_enable_social_media_behavior(self):
        title = u'Enable Social Media behavior'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # check state of previous version
        from plone.dexterity.interfaces import IDexterityFTI
        from sc.social.like.behaviors import ISocialMedia
        from zope.component import queryUtility
        enabled_portal_types = api.portal.get_registry_record(
            name='enabled_portal_types', interface=ISocialLikeSettings)

        # check behavior is not enabled for Dexterity-based content types
        for t in enabled_portal_types:
            fti = queryUtility(IDexterityFTI, name=t)
            if fti is None:
                continue  # not a Dexterity-based content type
            behaviors = list(fti.behaviors)
            self.assertNotIn(ISocialMedia.__identifier__, behaviors)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        # check behavior is now enabled for Dexterity-based content types
        for t in enabled_portal_types:
            fti = queryUtility(IDexterityFTI, name=t)
            if fti is None:
                continue  # not a Dexterity-based content type
            behaviors = list(fti.behaviors)
            self.assertIn(ISocialMedia.__identifier__, behaviors)


class To3046TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3045', u'3046')

    def test_upgrade_to_3046_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)

    @unittest.skipUnless(HAS_DEXTERITY, 'plone.app.contenttypes must be installed')
    def test_reindex_catalog(self):
        # check if the upgrade step is registered
        title = u'Reindex catalog'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        from sc.social.like.behaviors import ISocialMedia
        from sc.social.like.tests.utils import enable_social_media_behavior
        with api.env.adopt_roles(['Manager']):
            for i in xrange(0, 10):
                api.content.create(self.portal, 'News Item', str(i))

        # break the catalog by deleting an object without notifying
        self.portal._delObject('0', suppress_events=True)
        self.assertNotIn('0', self.portal)
        enable_social_media_behavior()
        results = api.content.find(object_provides=ISocialMedia.__identifier__)
        self.assertEqual(len(results), 0)

        # run the upgrade step to validate it
        self.request.set('test', True)  # avoid transaction commits on tests
        self.execute_upgrade_step(step)
        results = api.content.find(object_provides=ISocialMedia.__identifier__)
        self.assertEqual(len(results), 9)  # no failure and catalog updated
