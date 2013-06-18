# -*- coding:utf-8 -*-
from Products.Archetypes.interfaces import IBaseContent


def get_content_image(context, scale='large'):
    fields = ['image', 'leadImage', 'portrait']
    if IBaseContent.providedBy(context):
        schema = context.Schema()
        field = [field for field in schema.keys() if field in fields]
        if field:
            field = field[0]
    else:
        # Let's assume image as a valid fieldname
        field = 'image'
    try:
        view = context.unrestrictedTraverse('@@images')
        img = view.scale(fieldname=field, scale=scale)
    except AttributeError:
        img = None
    return img
