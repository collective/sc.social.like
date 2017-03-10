# -*- coding: utf-8 -*-
"""Package event subscribers.

Plone 5 includes a new social media configlet that duplicates some
records already included in this package. To deal with that we use
an event subscriber declared in this module to synchronize the values
of the redundant records on every change.
"""
from plone import api
from plone.registry.interfaces import IRegistry
from sc.social.like.config import IS_PLONE_5
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from zope.component import getUtility
from zope.schema.interfaces import WrongType


# redundant fields so far
FIELDS = ('facebook_app_id', 'facebook_username', 'twitter_username')

# used to avoid RuntimeError due to infinite recursion
_FLAG = False


def social_media_record_synchronizer(event):
    """Synchronize Plone 5 social media records if needed."""
    # subscribers are registered even if packages are not installed
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(PROJECTNAME):
        return

    if not IS_PLONE_5:
        return

    # check if we've been here before as part of same event processing
    global _FLAG
    if _FLAG:
        return

    logger.debug(u'Processing: ' + repr(event.record))
    field = event.record.fieldName
    if field not in FIELDS:
        logger.debug(u'Field name not being tracked')
        return

    # find out which record we need to synchronize
    from Products.CMFPlone.interfaces.controlpanel import ISocialMediaSchema
    interface = event.record.interfaceName
    if interface == ISocialLikeSettings.__identifier__:
        # sc.social.like record modified; synchronize Plone record
        record = 'plone.' + field
    elif interface == ISocialMediaSchema.__identifier__:
        # Plone record modified; synchronize sc.social.like record
        record = ISocialLikeSettings.__identifier__ + '.' + field
    else:
        logger.debug(u'Schema not being tracked')
        return

    registry = getUtility(IRegistry)
    # we're going to modify a record and this will fire the same event
    # we need to avoid RuntimeError due to infinite recursion
    _FLAG = True
    try:
        registry[record] = str(event.record.value)
    except WrongType:
        # Plone 5 declares records as TextLine
        registry[record] = unicode(event.record.value)
    _FLAG = False

    logger.debug('{0} was synchronized; new value is "{1}"'.format(
        repr(registry.records[record]), event.record.value))
