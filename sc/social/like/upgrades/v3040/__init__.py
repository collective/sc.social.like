# -*- coding:utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from zope.component import getUtility
from zope.schema.interfaces import ConstraintNotSatisfied


def update_configlet_information(setup_tool):
    """Update configlet information."""
    controlpanel = api.portal.get_tool(name='portal_controlpanel')
    configlet = controlpanel.getActionObject('Products/sociallikes')
    if configlet is not None:
        configlet.setActionExpression('string:${portal_url}/@@sociallike-settings')
        logger.info('Configlet information updated')


def _enforce_type_constraints(portal_types):
    """Return ReallyUserFriendlyTypes only. Old field values were not
    restricted in any way; new field values must be terms of this
    vocabulary.
    """
    from zope.component import getUtility
    from zope.schema.interfaces import IVocabularyFactory
    name = 'plone.app.vocabularies.ReallyUserFriendlyTypes'
    friendly_types = getUtility(IVocabularyFactory, name)(None)
    return tuple([i for i in portal_types if i in friendly_types])


def migrate_settings_to_registry(setup_tool):
    """Migrate settings to registry."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
    portal_properties = api.portal.get_tool(name='portal_properties')
    if 'sc_social_likes_properties' in portal_properties:
        old_props = portal_properties.sc_social_likes_properties
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialLikeSettings)
        # ignore types not allowed
        types_ = _enforce_type_constraints(old_props.enabled_portal_types)
        settings.enabled_portal_types = types_
        settings.plugins_enabled = old_props.plugins_enabled
        settings.typebutton = old_props.typebutton
        settings.do_not_track = old_props.do_not_track
        # this property may have an invalid value under certain circunstances
        try:
            settings.fbaction = old_props.fbaction
        except ConstraintNotSatisfied:  # empty string
            settings.fbaction = u'like'  # use default
        settings.fbbuttons = old_props.fbbuttons
        # these fields are no longer TextLine but ASCIILine
        # we need to avoid 'None' values caused by missing defaults
        settings.facebook_username = (
            str(old_props.fbadmins) if old_props.fbadmins else '')
        settings.facebook_app_id = (
            str(old_props.fbapp_id) if old_props.fbapp_id else '')
        settings.twitter_username = (
            str(old_props.twittvia) if old_props.twittvia else '')
        logger.info('Settings migrated')

        del portal_properties['sc_social_likes_properties']
        logger.info('Property sheet "sc_social_likes_properties" removed')
