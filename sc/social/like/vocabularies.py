# -*- coding:utf-8 -*-
from plone.memoize import forever
from sc.social.like import LikeMessageFactory as _
from sc.social.like.plugins import IPlugin
from zope.component import getUtilitiesFor
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class PluginsVocabulary(object):

    """Vocabulary factory listing available views."""

    @forever.memoize
    def plugins(self):
        terms = []
        registered = dict(getUtilitiesFor(IPlugin))
        keys = registered.keys()
        keys.sort()
        for key in keys:
            terms.append(SimpleTerm(key, title=key))

        return SimpleVocabulary(terms)

    def __call__(self, context):
        return self.plugins()

PluginsVocabularyFactory = PluginsVocabulary()


TypeButtonVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'horizontal', title=_(u'Horizontal')),
    SimpleTerm(value=u'vertical', title=_(u'Vertical')),
])

FacebookButtonsVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'Like', title=_(u'Like')),
    SimpleTerm(value=u'Share', title=_(u'Share')),
])

FacebookShareLayoutVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'box_count', title=_(u'Box Count')),
    SimpleTerm(value=u'button_count', title=_(u'Button Count')),
    SimpleTerm(value=u'button', title=_(u'Button')),
])

FacebookLikeActionVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'like', title=_(u'Like')),
    SimpleTerm(value=u'recommend', title=_(u'Recommend')),
])

FacebookLikeColorschemeVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'light', title=_(u'Light')),
    SimpleTerm(value=u'dark', title=_(u'Dark')),
])

FacebookLikeLayoutVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'standard', title=_(u'Standard')),
    SimpleTerm(value=u'box_count', title=_(u'Box Count')),
    SimpleTerm(value=u'button_count', title=_(u'Button Count')),
    SimpleTerm(value=u'button', title=_(u'Button')),
])

FacebookSizeVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'small', title=_(u'Small')),
    SimpleTerm(value=u'large', title=_(u'Large')),
])
