# -*- coding:utf-8 -*-
from Acquisition import aq_base
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFPlone.utils import safe_hasattr
from sc.social.like.logger import logger
from urlparse import urlparse
from zope.interface import Invalid


def get_images_view(context):
    view = context.unrestrictedTraverse('@@images', None)
    if view is None:
        return (None, None)
    if not IBaseContent.providedBy(context):
        return (view, 'image')
    fields = ['image', 'leadImage', 'portrait']
    schema = context.Schema()
    field = [f for f in schema.keys() if f in fields]
    if len(field) == 0:
        return (None, None)
    field = field[0]
    # if a content has an image field that isn't an ImageField (for example a relation field)
    if schema[field].type not in ['image', 'blob']:
        return (None, None)
    return (view, field)


def get_content_image(context):
    """Return image object just if we can get image size."""
    view, field = get_images_view(context)
    if view is None:
        return
    # XXX: If I recall correctly, Dexterity works different to do this
    try:
        sizes = view.getImageSize(field)
    except AttributeError:
        return
    if not sizes or sizes == (0, 0) or sizes == ('', ''):
        # this avoid strange cases where we can't get size infos.
        # for example if the loaded image in a news is a bmp or a tiff
        return
    try:
        return view.scale(fieldname=field, scale='large')
    except (AttributeError, TypeError):
        return


def get_language(context):
    ps = context.restrictedTraverse('plone_portal_state')
    default_language = ps.default_language()
    content = aq_base(context)
    if IBaseContent.providedBy(content):
        language = content.Language()
    else:
        language = content.language if safe_hasattr(content, 'language') else ''
    return language if language else default_language


def validate_canonical_domain(value):
    """Check if the value is a URI containing only scheme and netloc."""
    _ = urlparse(value)
    if not all([_.scheme, _.netloc]) or any([_.path, _.params, _.query, _.fragment]):
        raise Invalid(
            u'Canonical domain should only include scheme and netloc (e.g. <strong>http://www.example.org</strong>)')
    return True


def get_valid_objects(brains):
    """Generate a list of objects associated with valid brains."""
    for b in brains:
        try:
            obj = b.getObject()
        except KeyError:
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            msg = u'Skipping invalid reference in the catalog: {0}'
            logger.warn(msg.format(b.getPath()))
            continue
        yield obj
