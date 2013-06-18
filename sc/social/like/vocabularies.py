# -*- coding:utf-8 -*-
from plone.memoize import forever
from sc.social.like.plugins import IPlugin
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class PluginsVocabulary(object):
    """Vocabulary factory listing available views
    """

    implements(IVocabularyFactory)

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
