# -*- coding:utf-8 -*-
from plone import api
from sc.social.like.logger import logger


def cook_css_resources(context):  # pragma: no cover
    """Cook css resources."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.cookResources()
    logger.info('CSS resources were cooked')


def cook_javascript_resources(context):  # pragma: no cover
    """Cook javascript resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('Javascript resources were cooked')
