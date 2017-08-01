# -*- coding:utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.registry.interfaces import IRegistry
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from sc.social.like.utils import get_valid_objects
from zope.component import getUtility

import transaction


OPTIONS_TO_REMOVE = [
    '.fbaction',
    '.fbshowlikes',
]


def reindex_catalog(setup_tool):
    """Reindex objects to fix interfaces on the catalog."""
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info(
        u'Reindexing the catalog. '
        u'This process could take a long time on large sites. Be patient.'
    )
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog()
    logger.info(u'Found {0} objects'.format(len(results)))
    n = 0
    for obj in get_valid_objects(results):
        catalog.catalog_object(obj, idxs=['object_provides'], update_metadata=False)
        n += 1
        # XXX: https://github.com/gforcada/flake8-pep3101/issues/16
        if n % 1000 == 0 and not test:  # noqa: S001
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')


def update_facebook_options(context):
    """Update facebook options following new API."""
    logger.info(u'Update Action field.')
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISocialLikeSettings, check=False)

    record = ISocialLikeSettings.__identifier__ + '.fbaction'
    fbaction = registry.records[record].value
    loadMigrationProfile(
        context, 'sc.social.like:default', steps=['plone.app.registry'])
    settings.fblike_action = fbaction
    if settings.typebutton == 'horizontal' and 'Like' in settings.fbbuttons:
        settings.fblike_layout = 'button_count'
        settings.fblike_width = 90
    elif settings.typebutton == 'vertical' and 'Like' in settings.fbbuttons:
        settings.fblike_layout = 'box_count'
        settings.fblike_width = 55
    else:
        settings.fblike_layout = 'button'
        settings.fblike_width = 55

    logger.info(u'Remove old facebook options that don\'t exists anymore.')
    for option in OPTIONS_TO_REMOVE:
        record = ISocialLikeSettings.__identifier__ + option
        del registry.records[record]
        assert record not in registry
    logger.info('Done.')
