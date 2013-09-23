# -*- coding:utf-8 -*-
from Products.Archetypes.interfaces import IBaseContent
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest


def get_images_view(context):
    request = getRequest()
    key = "cache-view-%s" % (context)
    cache = IAnnotations(request)
    value = cache.get(key, None)
    if not value:
        view = context.unrestrictedTraverse('@@images', None)
        field = 'image'
        if view:
            fields = ['image', 'leadImage', 'portrait']
            if IBaseContent.providedBy(context):
                schema = context.Schema()
                field = [field for field in schema.keys() if field in fields]
                if field:
                    field = field[0]
                    if schema[field].type != "image":
                        field = ""
        value = (view, field) if (view and field) else (None, None)
        cache[key] = value
    return value


def get_content_image(context,
                      scale='large',
                      width=None,
                      height=None):
    request = getRequest()
    key = "cache-%s-%s-%s-%s" % (context, scale, width, height)
    cache = IAnnotations(request)
    img = cache.get(key, None)
    if not img:
        view, field = get_images_view(context)
        if view:
            kwargs = {}
            if not (width or height):
                kwargs['scale'] = scale
            else:
                if width:
                    kwargs['width'] = width
                if height:
                    kwargs['height'] = height
                kwargs['direction'] = 'down'
            try:
                img = view.scale(fieldname=field, **kwargs)
            except AttributeError:
                img = None
        cache[key] = img
    return img
