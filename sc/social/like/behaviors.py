# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ISocialMedia(model.Schema):
    """Social Media behavior."""

    canonical_url = schema.URI(
        title=u'Canonical URL',
        description=u'The canonical URL of the object that will be used as its permanent ID in the graph (og:url).',
        readonly=False,
        required=False,
    )
