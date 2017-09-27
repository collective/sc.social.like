# -*- coding:utf-8 -*-
from Acquisition import aq_base
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedBlobImage
from Products.Archetypes.interfaces import IBaseContent
from Products.CMFPlone.utils import safe_hasattr
from sc.social.like import LikeMessageFactory as _
from sc.social.like.config import OG_DESCRIPTION_MAX_LENGTH
from sc.social.like.config import OG_LEAD_IMAGE_MAX_SIZE
from sc.social.like.config import OG_LEAD_IMAGE_MIME_TYPES
from sc.social.like.config import OG_LEAD_IMAGE_MIN_ASPECT_RATIO
from sc.social.like.config import OG_LEAD_IMAGE_MIN_HEIGHT
from sc.social.like.config import OG_LEAD_IMAGE_MIN_WIDTH
from sc.social.like.config import OG_TITLE_MAX_LENGTH
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


MSG_INVALID_OG_TITLE = _(
    u'Title of content should have less than 70 characters.')


def validate_og_title(title):
    """Check if title of content is set and has less than 70 characters.

    More information:
    * https://dev.twitter.com/cards/markup
    """
    if title and len(title) <= OG_TITLE_MAX_LENGTH:
        return True

    raise ValueError(MSG_INVALID_OG_TITLE)


MSG_INVALID_OG_DESCRIPTION = _(
    u'Description of content should have less than 200 characters.')


def validate_og_description(description):
    """Check if description of content and has less than 200 characters.
    Facebook recomends at least two sentences long, but we will not
    enforce that for now.

    More information:
    * https://dev.twitter.com/cards/markup
    * https://developers.facebook.com/docs/sharing/best-practices
    """
    if not description or len(description) <= OG_DESCRIPTION_MAX_LENGTH:
        return True

    raise ValueError(MSG_INVALID_OG_DESCRIPTION)


MSG_INVALID_OG_LEAD_IMAGE_MIME_TYPE = _(u'Lead image MIME type not supported.')
MSG_INVALID_OG_LEAD_IMAGE_SIZE = _(u'Lead image size should be less than 5MB.')
MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS = _(
    u'Lead image should be at least 600px width and 315px height.')
MSG_INVALID_OG_LEAD_IMAGE_ASPECT_RATIO = _(
    u'Lead image aspect ratio should be at least 1.33:1.')


# XXX: current implementation makes hard testing the validator
def validate_og_lead_image(image):
    """Check if lead image scale follows best practices on MIME type,
    size, dimensions and aspect ratio.

    More information:
    * https://dev.twitter.com/cards/markup
    * https://developers.facebook.com/docs/sharing/best-practices

    :param image: lead image scale object
    :type image: instance of plone.namedfile.scaling.ImageScale
    :returns: True if the image follows best practices
    :rtype: bool
    :raises ValueError: if image doesn't follow best practices
    """
    if image is None:
        return True

    if image.mimetype not in OG_LEAD_IMAGE_MIME_TYPES:
        raise ValueError(MSG_INVALID_OG_LEAD_IMAGE_MIME_TYPE)

    if image.data.size > OG_LEAD_IMAGE_MAX_SIZE:
        raise ValueError(MSG_INVALID_OG_LEAD_IMAGE_SIZE)

    width, height = image.width, image.height
    if width < OG_LEAD_IMAGE_MIN_WIDTH or height < OG_LEAD_IMAGE_MIN_HEIGHT:
        raise ValueError(MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)

    aspect_ratio = float(image.width) / float(image.height)
    if aspect_ratio < OG_LEAD_IMAGE_MIN_ASPECT_RATIO:
        raise ValueError(MSG_INVALID_OG_LEAD_IMAGE_ASPECT_RATIO)

    return True


def validate_og_fallback_image(value):
    """Check if fallback image follows best practices on MIME type,
    size, dimensions and aspect ratio.
    """
    if value is None:
        return True

    filename, data = b64decode_file(value)
    image = NamedBlobImage(data=data, filename=filename)

    if image.contentType not in OG_LEAD_IMAGE_MIME_TYPES:
        raise Invalid(MSG_INVALID_OG_LEAD_IMAGE_MIME_TYPE)

    if image.getSize() > OG_LEAD_IMAGE_MAX_SIZE:
        raise Invalid(MSG_INVALID_OG_LEAD_IMAGE_SIZE)

    width, height = image.getImageSize()
    if width < OG_LEAD_IMAGE_MIN_WIDTH or height < OG_LEAD_IMAGE_MIN_HEIGHT:
        raise Invalid(MSG_INVALID_OG_LEAD_IMAGE_DIMENSIONS)

    aspect_ratio = float(width) / float(height)
    if aspect_ratio < OG_LEAD_IMAGE_MIN_ASPECT_RATIO:
        raise Invalid(MSG_INVALID_OG_LEAD_IMAGE_ASPECT_RATIO)

    return True
