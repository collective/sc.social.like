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


def migrate_settings_to_registry(setup_tool):  # noqa: C901
    """Migrate settings to registry."""

    def filter_types(portal_types):
        """Return ReallyUserFriendlyTypes only. Old field values were
        not restricted in any way; new field values must be terms of
        this vocabulary.
        """
        from zope.component import getUtility
        from zope.schema.interfaces import IVocabularyFactory
        name = 'plone.app.vocabularies.ReallyUserFriendlyTypes'
        friendly_types = getUtility(IVocabularyFactory, name)(None)
        return tuple([i for i in portal_types if i in friendly_types])

    def safe_migrate(old_attr, new_attr=None, to_string=False):
        """Copy value for property sheet to registry record avoiding
        AttributeError; rename record if needed. In case of error
        the record must already have loaded its default value.
        """
        try:
            value = getattr(old_props, old_attr)
        except AttributeError:
            pass

        if to_string:  # convert unicode to string?
            # avoid 'None' on None values (missing value)
            value = str(value) if value else ''

        if new_attr is None:
            new_attr = old_attr
        setattr(settings, new_attr, value)

    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
    portal_properties = api.portal.get_tool(name='portal_properties')
    if 'sc_social_likes_properties' not in portal_properties:
        logger.warn('Property sheet not found; using defaults')
        return

    old_props = portal_properties.sc_social_likes_properties
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISocialLikeSettings)

    # ignore types not allowed
    try:
        portal_types = old_props.enabled_portal_types
    except AttributeError:
        pass
    else:
        portal_types = filter_types(portal_types)
        settings.enabled_portal_types = portal_types

    safe_migrate('plugins_enabled')
    safe_migrate('typebutton')
    safe_migrate('do_not_track')

    try:
        safe_migrate('fbaction')
    except ConstraintNotSatisfied:
        pass  # skip on empty string

    safe_migrate('fbbuttons')

    # these fields are no longer TextLine but ASCIILine
    # and have a different name
    safe_migrate('fbadmins', 'facebook_username', to_string=True)
    safe_migrate('fbapp_id', 'facebook_app_id', to_string=True)
    safe_migrate('twittvia', 'twitter_username', to_string=True)

    logger.info('Settings migrated')

    del portal_properties['sc_social_likes_properties']
    logger.info('Property sheet removed')
