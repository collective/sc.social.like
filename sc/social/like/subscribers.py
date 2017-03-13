# -*- coding: utf-8 -*-
"""Event subscribers.

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

import traceback


# redundant fields so far
FIELDS = ('facebook_app_id', 'facebook_username', 'twitter_username')

# used to deal with recursion
FN_NAME = 'social_media_record_synchronizer'


def social_media_record_synchronizer(event):
    """Synchronize Plone 5 social media records if needed.

    An aditional IRecordModifiedEvent is fired by this function; we
    deal with that to avoid RuntimeError due to infinite recursion.
    """
    # how many times the name of this function appears on the stack?
    stack = [l[2] for l in traceback.extract_stack() if l[2] == FN_NAME]
    if len(stack) > 1:
        return  # we've been here before

    # subscribers are registered even if packages are not installed
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(PROJECTNAME):
        return

    if not IS_PLONE_5:
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
    # this will fire the aditional IRecordModifiedEvent
    try:
        registry[record] = str(event.record.value)
    except WrongType:
        # Plone 5 declares records as TextLine
        registry[record] = unicode(event.record.value)

    logger.debug('{0} was synchronized; new value is "{1}"'.format(
        repr(registry.records[record]), event.record.value))
