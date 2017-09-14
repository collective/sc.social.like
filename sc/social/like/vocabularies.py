# -*- coding:utf-8 -*-
from plone.app.imaging.utils import getAllowedSizes
from plone.memoize import forever
from sc.social.like import LikeMessageFactory as _
from sc.social.like.plugins import IPlugin
from zope.component import getUtilitiesFor
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# ADD IN CONFIG.PY
LEAD_IMAGE_MIN_ASPECT_RATIO = 1.33
LEAD_IMAGE_MIN_HEIGHT = 315
LEAD_IMAGE_MIN_WIDTH = 600


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
    SimpleTerm(value=u'horizontal', title=_(u'horizontal')),
    SimpleTerm(value=u'vertical', title=_(u'vertical')),
])


FacebookVerbsVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'like', title=_(u'Like')),
    SimpleTerm(value=u'recommend', title=_(u'Recommend')),
])

FacebookButtonsVocabulary = SimpleVocabulary([
    SimpleTerm(value=u'Like', title=_(u'Like')),
    SimpleTerm(value=u'Share', title=_(u'Share')),
])


@provider(IVocabularyFactory)
def ImageScalesVocabulary(object):
    """Obtains available scales from plone.app.imaging"""
    terms = []
    for scale, (width, height) in getAllowedSizes().iteritems():
        if width >= LEAD_IMAGE_MIN_WIDTH and height >= LEAD_IMAGE_MIN_HEIGHT:
            translated = _(
                'imagescale_{0:s}'.format(scale),
                default='{0:s} ${{width}}x${{height}}'.format(scale),
                mapping={'width': str(width), 'height': str(height)})
            terms.append(SimpleTerm(scale, scale, translated))

    return SimpleVocabulary(terms)
