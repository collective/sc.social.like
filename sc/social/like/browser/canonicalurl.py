# -*- coding:utf-8 -*-
from plone import api
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.logger import logger
from sc.social.like.utils import validate_canonical_domain
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema


def get_valid_objects(brains):
    """Generate a list of objects associated with valid brains."""
    for b in brains:
        try:
            obj = b.getObject()
        except KeyError:
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            logger.warn(
                u'Invalid reference in the catalog: {0}'.format(b.getPath()))
            continue
        yield obj


class ICanonicalURLUpdater(model.Schema):
    """A form to update the canonical url of portal objects based on a date."""

    canonical_domain = schema.URI(
        title=_(u'Canonical domain'),
        description=_(
            u'help_canonical_domain',
            default=u'The canonical domain will be used to construct the canonical URL (<code>og:url</code> property) of portal objects. '
                    u'Use the domain name of your site (e.g. <strong>http://www.example.org</strong> or <strong>https://www.example.org</strong>). '
                    u'Facebook will use the canonical URL to ensure that all actions such as likes and shares aggregate at the same URL rather than spreading across multiple versions of a page. '
                    u'Check <a href="https://pypi.python.org/pypi/sc.social.like">package documentation</a> for more information on how to use this feature.'
        ),
        required=True,
        constraint=validate_canonical_domain,
    )

    created_before = schema.Date(
        title=_(u'Date'),
        description=_(
            u'help_date',
            u'All objects in the catalog created before this date will be updated.'
        ),
        required=True,
    )


class CanonicalURLUpdater(form.Form):
    """A form to update the canonical url of portal objects based on a date."""

    fields = field.Fields(ICanonicalURLUpdater)
    label = _(u'This form is used to update the canonical URL of objects providing the Social Media behavior')
    ignoreContext = True

    def update(self):
        """Disable the green bar and the portlet columns."""
        super(CanonicalURLUpdater, self).update()
        self.request.set('disable_border', 1)
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    @button.buttonAndHandler(_('Update'), name='update')
    def handle_update(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _(u'Please correct the errors.')
            return

        self.update_canonical_url(data)

    @button.buttonAndHandler(_(u'label_cancel', default=u'Cancel'), name='cancel')
    def handle_cancel(self, action):
        self.request.response.redirect(self.context.absolute_url())

    def update_canonical_url(self, data):
        """Update all objects providing the ISocialMedia behavior
        that were created before the specified date.
        """
        canonical_domain = data['canonical_domain']
        created_before = data['created_before'].isoformat()
        logger.info(
            u'Updating canonical URL of items created before {0}; '
            u'using canonical domain "{1}"'.format(created_before, canonical_domain)
        )

        catalog = api.portal.get_tool('portal_catalog')
        results = catalog(
            object_provides=ISocialMedia.__identifier__,
            created=dict(query=created_before, range='max'),
        )

        total = len(results)
        logger.info(u'{0} objects will be processed'.format(total))
        for obj in get_valid_objects(results):
            obj.canonical_url = '{0}/{1}'.format(canonical_domain, obj.virtual_url_path())

        logger.info(u'Done.')
        self.status = u'Update complete; {0} items processed.'.format(total)
