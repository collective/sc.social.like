# -*- coding: utf-8 -*-
"""Event subscribers.

Plone 5 includes a new social media configlet that duplicates some
records already included in this package. To deal with that we use
an event subscriber declared in this module to synchronize the values
of the redundant records on every change.

Facebook needs a canonical URL to ensure that all actions such as likes
and shares aggregate at the same URL rather than spreading across
multiple versions of a page. We populate a field with this value at
creation time using an event handler bounded to IObjectAddedEvent
because on IObjectCreatedEvent the container of the object is not
available and we can not get its virtual path.
"""

from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.utils import get_installer
from sc.social.like.config import IS_PLONE_5
from sc.social.like.config import PROJECTNAME
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from sc.social.like.utils import get_content_image
from sc.social.like.utils import validate_og_description
from sc.social.like.utils import validate_og_lead_image
from sc.social.like.utils import validate_og_title
from zope.component import getUtility

import requests
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
    stack = [fr[2] for fr in traceback.extract_stack() if fr[2] == FN_NAME]
    if len(stack) > 1:
        return  # we've been here before

    # subscribers are registered even if packages are not installed
    # so we must check whether we are installed before proceeding.
    qi = get_installer(api.portal.get())
    if not qi.is_product_installed(PROJECTNAME):
        return

    if not IS_PLONE_5:
        return

    logger.debug('Processing: ' + repr(event.record))
    field = event.record.fieldName
    if field not in FIELDS:
        logger.debug('Field name not being tracked')
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
        logger.debug('Schema not being tracked')
        return

    registry = getUtility(IRegistry)
    # this will fire the aditional IRecordModifiedEvent
    registry[record] = str(event.record.value)

    logger.debug('{0} was synchronized; new value is "{1}"'.format(
        repr(registry.records[record]), event.record.value))


def check_sharing_best_practices(obj, event):
    """Check if content follows social networks sharing best practices
    as defined by Twitter and Facebook.
    """
    record = ISocialLikeSettings.__identifier__ + '.validation_enabled'
    validation_enabled = api.portal.get_registry_record(record, default=False)
    if not validation_enabled:
        return

    try:
        review_state = api.content.get_state(obj)
    except WorkflowException:
        # images and files have no associated workflow by default
        review_state = 'published'

    if review_state not in ('published', ):
        return  # no need to validate

    request = obj.REQUEST

    title = getattr(obj, 'title', '')
    try:
        validate_og_title(title)
    except ValueError as e:
        api.portal.show_message(message=str(e), request=request, type='warning')

    description = getattr(obj, 'description', '')
    try:
        validate_og_description(description)
    except ValueError as e:
        api.portal.show_message(message=str(e), request=request, type='warning')

    image = get_content_image(obj)
    try:
        validate_og_lead_image(image)
    except ValueError as e:
        api.portal.show_message(message=str(e), request=request, type='warning')


def facebook_prefetching(obj, event):
    """Call Facebook Graph API endpoint to keep metadata of published
    objects always updated.
    """
    record = ISocialLikeSettings.__identifier__ + '.facebook_prefetch_enabled'
    prefetch_enable = api.portal.get_registry_record(record, default=False)
    if not prefetch_enable:
        return

    try:
        review_state = api.content.get_state(obj)
    except WorkflowException:
        # images and files have no associated workflow by default
        review_state = 'published'

    if review_state not in ('published', ):
        return  # can't prefetch non-public content

    url = obj.absolute_url()
    endpoint = 'https://graph.facebook.com/?id=' + url + '&scrape=true'
    try:
        r = requests.post(endpoint, timeout=5)
    except requests.exceptions.RequestException as e:
        logger.warning('Prefetch failure: %s', e)
        return

    if r.status_code == '200':
        logger.info('Prefetch successful: %s', url)
    else:
        logger.warning(
            'Prefetch error {code} ({reason}): {debug}'.format(
                code=r.status_code, reason=r.reason, debug=str(r.json())))
