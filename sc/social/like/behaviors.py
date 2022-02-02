# -*- coding: utf-8 -*-
"""In the future this behavior will control in which content types we
will display the Social Media widgets, replacing the
``enabled_portal_types`` field in the control panel configlet.
"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import provider


@provider(IFormFieldProvider)
class ISocialMedia(model.Schema):
    """Social Media behavior."""
    # The canonical URL behavior is already provided by Plone 6 core.
    # This interface is left for backwards compatibility, and for
    # the future plans to use it as marking which objects are to be
    # social-media'd -- as described somewhere else in the code.
