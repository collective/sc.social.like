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
        keys = list(registered.keys())
        keys.sort()
        for key in keys:
            terms.append(SimpleTerm(key, title=key))

        return SimpleVocabulary(terms)

    def __call__(self, context):
        return self.plugins()


PluginsVocabularyFactory = PluginsVocabulary()


TypeButtonVocabulary = SimpleVocabulary([
    SimpleTerm(value='horizontal', title=_('horizontal')),
    SimpleTerm(value='vertical', title=_('vertical')),
])


FacebookVerbsVocabulary = SimpleVocabulary([
    SimpleTerm(value='like', title=_('Like')),
    SimpleTerm(value='recommend', title=_('Recommend')),
])

FacebookButtonsVocabulary = SimpleVocabulary([
    SimpleTerm(value='Like', title=_('Like')),
    SimpleTerm(value='Share', title=_('Share')),
])
