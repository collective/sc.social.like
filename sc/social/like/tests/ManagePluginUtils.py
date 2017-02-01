# -*- coding: utf-8 -*-
"""Helper function to manage sc.social.like plugins."""
from plone import api
from sc.social.like.interfaces import ISocialLikeSettings

import transaction


def enable_plugin(plugin):
    """Enable sc.social.like plugins."""
    record = dict(name='plugins_enabled', interface=ISocialLikeSettings)
    plugins_enabled = api.portal.get_registry_record(**record)
    record['value'] = plugins_enabled + (plugin, )
    api.portal.set_registry_record(**record)
    transaction.commit()


def disable_plugin(plugin):
    """Disable sc.social.like plugins."""
    record = dict(name='plugins_enabled', interface=ISocialLikeSettings)
    plugins_enabled = api.portal.get_registry_record(**record)
    record['value'] = tuple(p for p in plugins_enabled if p != plugin)
    api.portal.set_registry_record(**record)
    transaction.commit()
