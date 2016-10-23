# -*- coding: utf-8 -*-
"""Hacks to work around API inconsistencies between Archetypes and Dexterity."""


def set_image_field(obj, image, content_type):
    """Set image field in object on both, Archetypes and Dexterity."""
    try:
        obj.setImage(image)  # Archetypes
    except AttributeError:
        # Dexterity
        from plone.namedfile.file import NamedBlobImage
        data = image if type(image) == str else image.getvalue()
        obj.image = NamedBlobImage(data=data, contentType=content_type)
    finally:
        obj.reindexObject()


def set_file_field(obj, file, content_type):
    """Set file field in object on both, Archetypes and Dexterity."""
    try:
        obj.setFile(file)  # Archetypes
    except AttributeError:
        # Dexterity
        from plone.namedfile.file import NamedBlobFile
        obj.file = NamedBlobFile(data=file, contentType=content_type)
    finally:
        obj.reindexObject()


def set_text_field(obj, text):
    """Set text field in object on both, Archetypes and Dexterity."""
    try:
        obj.setText(text)  # Archetypes
    except AttributeError:
        from plone.app.textfield.value import RichTextValue
        obj.text = RichTextValue(text, 'text/html', 'text/html')  # Dexterity
    finally:
        obj.reindexObject()
