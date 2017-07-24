# -*- coding:utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.supermodel import model
from sc.social.like import LikeMessageFactory as _
from sc.social.like.behaviors import ISocialMedia
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.logger import logger
from sc.social.like.utils import get_valid_objects
from sc.social.like.utils import validate_canonical_domain
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema


class ICanonicalURLUpdater(model.Schema):
    """A form to update the canonical url of portal objects based on a date."""

    old_canonical_domain = schema.URI(
        title=_(u'Old canonical domain'),
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

    published_before = schema.Date(
        title=_(u'Date'),
        description=_(
            u'help_published_before',
            default=u'Objects published before this date will be updated using the canonical domain defined in this form; '
                    u'objects published on or after this date will be updated using the canonical domain defined in the control panel configlet.'
        ),
        required=True,
    )


class CanonicalURLUpdater(form.Form):
    """A form to update the canonical url of portal objects based on a date."""

    fields = field.Fields(ICanonicalURLUpdater)
    label = _(u'Canonical URL updater form')
    description = _(
        u'This form will update the canonical URL of all Dexterity-based '
        u'objects in the catalog providing the Social Media behavior.'
    )
    ignoreContext = True

    @property
    def canonical_domain(self):
        return api.portal.get_registry_record(name='canonical_domain', interface=ISocialLikeSettings)

    def update(self):
        super(CanonicalURLUpdater, self).update()
        # show error message if no canonical domain has been defined in the configlet
        if not self.canonical_domain:
            msg = _(u'Canonical domain has not been defined in the control panel configlet.')
            api.portal.show_message(message=msg, request=self.request, type='error')

        # disable the green bar and the portlet columns
        self.request.set('disable_border', 1)
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    @property
    def update_button_enabled(self):
        """Condition to be used to display the "Update" button."""
        return self.canonical_domain is not None

    @button.buttonAndHandler(_('Update'), name='update', condition=lambda form: form.update_button_enabled)
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
        """Update the canonical URL of all objects in the catalog
        providing the ISocialMedia behavior.

        Objects published before the specified date will be updated
        using the canonical domain defined in this form; objects
        published on or after that date will be updated using the
        canonical domain defined in the control panel configlet.
        """
        old_canonical_domain = data['old_canonical_domain']
        new_canonical_domain = self.canonical_domain
        published_before = data['published_before'].isoformat()
        results = api.content.find(
            object_provides=ISocialMedia.__identifier__,
            review_state='published',
        )
        total = len(results)
        logger.info(u'{0} objects will have their canonical URL updated'.format(total))

        for obj in get_valid_objects(results):
            # FIXME: we're currently ignoring the Plone site id
            #        https://github.com/collective/sc.social.like/issues/119
            path = '/'.join(obj.getPhysicalPath()[2:])
            if obj.effective_date < DateTime(published_before):
                # use the canonical domain defined in this form
                obj.canonical_url = '{0}/{1}'.format(old_canonical_domain, path)
            elif not obj.canonical_url:
                # use the canonical domain defined in the configlet
                obj.canonical_url = '{0}/{1}'.format(new_canonical_domain, path)

        logger.info(u'Done.')
        self.status = u'Update complete; {0} items processed.'.format(total)
