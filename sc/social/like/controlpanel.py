# -*- coding:utf-8 -*-
from plone.app.registry.browser import controlpanel
from sc.social.like import LikeMessageFactory as _
from sc.social.like.interfaces import ISocialLikeSettings


class SocialLikeSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = ISocialLikeSettings
    label = _('Social Like')
    description = _('Settings for the sc.social.like package')


class SocialLikeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = SocialLikeSettingsEditForm
