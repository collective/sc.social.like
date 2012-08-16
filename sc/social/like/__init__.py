# -*- coding: utf-8 -*-

"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
LikeMessageFactory = MessageFactory('sc.social.like')


def initialize(context):
    """Initializer called when used as a Zope 2 product.
    """
