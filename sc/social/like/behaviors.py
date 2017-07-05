# -*- coding: utf-8 -*-
"""In the future this behavior will control in which content types we
will display the Social Media widgets, replacing the
``enabled_portal_types`` field in the control panel configlet.
"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ISocialMedia(model.Schema):
    """Social Media behavior."""

    # TODO: move field to "settings" fieldset
    canonical_url = schema.URI(
        title=_(u'Canonical URL'),
        description=_(
            u'help_canonical_url',
            default=u'The canonical URL of the object that will be used as its permanent ID in the graph (<code>og:url</code>).',
        ),
        readonly=True,
        required=False,
    )
