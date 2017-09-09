# -*- coding:utf-8 -*-
from Acquisition import aq_base
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFPlone.utils import safe_hasattr
from sc.social.like.logger import logger
from urlparse import urlparse
from zope.interface import Invalid


def get_images_view(context):
    view = context.unrestrictedTraverse('@@images', None)
    field = 'image'
    if view:
        fields = ['image', 'leadImage', 'portrait']
        if IBaseContent.providedBy(context):
            schema = context.Schema()
            field = [f for f in schema.keys() if f in fields]
            if field:
                field = field[0]
                # if a content has an image field that isn't an ImageField
                # (for example a relation field), set field='' to avoid errors
                if schema[field].type not in ['image', 'blob']:
                    field = ''
    return (view, field) if (view and field) else (None, None)


def get_content_image(context,
                      scale='large',
                      width=None,
                      height=None):
    view, field = get_images_view(context)
    img = None
    if view:
        try:
            sizes = view.getImageSize(field)
        except AttributeError:
            sizes = img = None
        if sizes == (0, 0) or sizes == ('', ''):
            # this avoid strange cases where we can't get size infos.
            # for example if the loaded image in a news is a bmp or a tiff
            return None
        if sizes:
            kwargs = {}
            if not (width or height):
                kwargs['scale'] = scale
            else:
                new = (width, height)
                width, height = _image_size(sizes, new)
                kwargs['width'] = width
                kwargs['height'] = height
                kwargs['direction'] = 'down'
            try:
                img = view.scale(fieldname=field, **kwargs)
            except (AttributeError, TypeError):
                img = None
    return img


def get_language(context):
    ps = context.restrictedTraverse('plone_portal_state')
    default_language = ps.default_language()
    content = aq_base(context)
    if IBaseContent.providedBy(content):
        language = content.Language()
    else:
        language = content.language if safe_hasattr(content, 'language') else ''
    return language if language else default_language


def _image_size(current, new):
    # Current width, height and aspect ratio
    c_width, c_height = current
    if not (c_width and c_height):
        return (0, 0)
    c_aspect = float(c_width) / float(c_height)
    # New width, height
    n_width, n_height = new

    # If new dimensions are larger than the current ones, we
    # return the current dimensions
    if (n_width > c_width) or (n_height > c_height):
        return current
    width = n_width
    height = int(round(float(width) / c_aspect))
    if n_height > height:
        height = n_height
        width = int(round(height * c_aspect))
        if n_width > width:
            return current
    return (width, height)


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


def validate_title_social(value):
    """Check if title field have more than 70 characters."""
    if len(value) > 70:
        msg = u'Title have more than 70 characters.'
        logger.info(msg)
        return msg
    return


def validate_description_social(value):
    """Check if description field have more than 200 characters."""

    if value and len(value) > 200:
        msg = u'Description have more than 200 characters.'
        logger.info(msg)
        return msg

    elif value and (value.count('.') < 2 or value.count('.') > 2):
        msg = u'Description should contain at least 2 phrases.'
        logger.info(msg)
        return msg

    return


def validate_image_social(value):
    """Check if image be in formats mime type, dimensions and size."""

    list_mimetypes = ['image/jpeg', 'image/png', 'image/gif', ' image/webp']

    if value.mimetype not in list_mimetypes:
        msg = u'Image mime type not supported: {0}'
        logger.info(msg.format(type))
        return msg.format(type)

    try:
        size = value.size
    except AttributeError:
        size = value.data.size
    if size > 5242880:
        msg = u'Image size should be less than 5MB.'
        logger.info(msg)
        return msg

    width, height = (value.width, value.height)
    if width < 600 or height < 315:
        msg = u'Image dimensions should be at least 600 x 315.'
        logger.info(msg)
        return msg

    if get_ratio(width, height) < 1.33:
        msg = u'Image aspect ratio should be 1.33:1 at least.'
        logger.info(msg)
        return msg


def get_ratio(w, h):
    """Calculate aspect ratio."""
    w = float(w)
    h = float(h)
    r = (w % h) or w
    return '{0:.2f}'.format(float((w / r) / (h / r)))
