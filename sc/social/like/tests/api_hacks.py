# -*- coding: utf-8 -*-
"""Hacks to work around API inconsistencies between Archetypes and Dexterity."""


def set_image_field(obj, image, content_type):
    """Set image field in object on both, Archetypes and Dexterity."""
    from plone.namedfile.file import NamedBlobImage
    try:
        obj.setImage(image)  # Archetypes
    except AttributeError:
        # Dexterity
        if type(image) == str:
            data = bytes(image, 'utf-8')
        elif type(image) == bytes:
            data = image
        else:
            data = image.getvalue()
        obj.image = NamedBlobImage(data=data, contentType=content_type)
    finally:
        obj.reindexObject()
