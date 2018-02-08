# -*- coding:utf-8 -*-
from plone import api
from sc.social.like.logger import logger
from sc.social.like.utils import get_valid_objects

import transaction


def reindex_catalog(setup_tool):
    """Reindex objects to fix interfaces on the catalog."""
    test = 'test' in setup_tool.REQUEST  # used to ignore transactions on tests
    logger.info(
        u'Reindexing the catalog. '
        u'This process could take a long time on large sites. Be patient.')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog()
    logger.info(u'Found {0} objects'.format(len(results)))
    n = 0
    for obj in get_valid_objects(results):
        catalog.catalog_object(obj, idxs=['object_provides'], update_metadata=False)
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        transaction.commit()
    logger.info('Done.')
