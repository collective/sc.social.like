# -*- coding:utf-8 -*-
from plone import api
from sc.social.like.logger import logger
from sc.social.like.utils import get_valid_objects

import transaction

try:
    # this exception must be resubmitted:
    from ZODB.POSException import ConflictError
except ImportError:
    # we don't really *require* this;
    #  if we don't have it, a dummy exception will do:
    class ConflictError(Exception):
        pass


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
    errors = 0
    for obj in get_valid_objects(results):
        try:
            catalog.catalog_object(obj, idxs=['object_provides'], update_metadata=False)
        except ConflictError:
            raise
        except Exception as e:
            errors += 1
            logger.error('{0!r} reindexing {1!r}'.format(e, obj))
            if test:
                raise
        n += 1
        if n % 1000 == 0 and not test:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    if not test:
        if errors:
            logger.info('{0} errors occured.'.format(errors))
        transaction.commit()
    logger.info('Done.')
