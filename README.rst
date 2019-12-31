=====================================
Social networks integration for Plone
=====================================

.. contents:: Table of Contents
   :depth: 2


Life, the Universe, and Everything
----------------------------------

This package provides integration with the following social networks in Plone:

* Facebook
* Google+
* LinkedIn
* Pinterest
* Telegram
* Twitter
* WhatsApp (mobile only)

The integration is done via `Open Graph protocol <http://ogp.me/>`_ basic metadata and the inclusion of sharing widgets for all enabled social networks.

Mostly Harmless
---------------

.. image:: http://img.shields.io/pypi/v/sc.social.like.svg
    :target: https://pypi.python.org/pypi/sc.social.like

.. image:: https://img.shields.io/travis/collective/sc.social.like/master.svg
    :target: http://travis-ci.org/collective/sc.social.like

.. image:: https://img.shields.io/coveralls/collective/sc.social.like/master.svg
    :target: https://coveralls.io/r/collective/sc.social.like

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/sc.social.like/issues

Don't Panic
-----------

Plone version compatibility
---------------------------

This package is compatible with Plone 4.3 and 5.0.

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``sc.social.like`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        sc.social.like

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``Social: Like Actions`` and click the 'Activate'
button.

Configuration
^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Social Like' link -- under Add-on Configuration.

.. figure:: https://github.com/collective/sc.social.like/raw/master/docs/control-panel.png
    :align: center
    :height: 1024px
    :width: 768px

    The control panel configlet.

There you can configure how **Social: Like Actions** will behave, which actions
will be displayed and for which content types.

Open Graph protocol support
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following basic metadata is included on content types with Social Media behavior enabled:

* ``og:title``: the title of the item
* ``og:description``: the description of the item
* ``og:type``: defaults to 'website' on the portal root and 'article' elsewhere
* ``og:url``: the canonical URL of the item, that is the URL used by the item when it was first published
* ``og:image``: the 'large' scale of the lead image of the item, if present;
  you can define a fallback image to be used in content that lacks lead image on the control panel configlet

Validation of best practices for social networks sharing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This feature is only available for Dexterity-based content types.

A content validation process is executed every time you publish an item, or when you edit an item in the ``published`` state.
This process includes checking of maximum length of title and description fields, as well as format, size and dimensions of the lead image field, if present.
A warning message will be shown to the user if the content does not comply with best practices.

Sharing best practices were compiled mainly from Twitter and Facebook recommendations.
For more information see:

* https://dev.twitter.com/cards/markup
* https://developers.facebook.com/docs/sharing/best-practices

You can disable content validation using an option in the control panel configlet.

Facebook prefetch
^^^^^^^^^^^^^^^^^

.. note::
    This feature is only available for Dexterity-based content types.

When content is shared for the first time,
the Facebook crawler will scrape and cache the metadata from the URL shared.
The crawler has to see images at least once before they can be rendered.
Prefetching allows Facebook to download content before someone shares it.

According to `Facebook's documentation <https://www.facebook.com/business/help/1514372351922333>`_,
prefetching is especially beneficial for people using Facebook on slow or poor network connections.
Prefetching also loads mobile site content faster,
which improves the Facebook app experience on Android and iPhone devices.

You can enable Facebook prefetch using an option in the control panel configlet.

A call to the Graph API endpoint will be generated automatically every time a new piece content is published,
and every time a published content is edited.
This will keep the metadata updated on Facebook always.

Canonical URL and migration to HTTPS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
    This feature is only available for Dexterity-based content types.
    If you're using Archetypes-based content types or if you don't apply the Social Media behavior to your Dexterity-based content type,
    the current URL will still be used as the canonical URL.

The first time someone shares a link, the Facebook crawler will scrape the HTML code at that URL to gather, cache and display info about the content on Facebook.
Facebook uses the ``og:url`` tag included in the HTML code to aggregate likes and shares at the same URL rather than spreading across multiple versions of a page.
If you move your content around or if you migrate your site schema from HTTP to HTTPS those counters will be zeroed.

To solve this issue this package includes a mechanism to store the URL of the content at publication time to use it as the canonical URL even after renaming or migrating the schema.
To enable this feature you must apply the Social Media behavior to your content type and provide the canonical domain (e.g. ``http://www.example.org``) to be used on the site in the control panel configlet.

If you later migrate your site to HTTPS just change the value of the canonical domain (e.g. ``https://www.example.org``).
All content created before the change will still reflect the old schema in their canonical url as expected.

The package also includes a helper view to populate content created before release 2.10.
You can access this view by pointing your browser at ``/@@canonical-url-updater``.

Privacy and cookies
^^^^^^^^^^^^^^^^^^^

Social media widgets commonly track user actions and add third party cookies.

If privacy is something you must care about
(for instance, if you need to comply with the `European Cookie Law <http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32009L0136>`_),
sc.social.like provides a "*Do not track users*" option.
When enabled, social media widgets will be rendered as simple HTML links at the expense of features and user experience.

This product is also respects the `Do Not Track <http://donottrack.us/>`_ user's browser preference.
If the user configured the browser for not being tracked,
social media will be rendered as if the "*Severe privacy*" setting was enabled.

Social media and Plone 5
^^^^^^^^^^^^^^^^^^^^^^^^

Plone 5 includes some configuration fields already available in this package on a new Social Media configlet.
A synchronization of the values of those redundant fields takes place behind the scenes every time you change the Twitter username, the Facebook App ID or the Facebook username,
using either the new Social Media configlet or the Social Like configlet.

.. figure:: https://github.com/collective/sc.social.like/raw/master/docs/social-media-configlet.png
    :align: center
    :height: 560px
    :width: 768px

    The Social Media configlet in Plone 5.

Screenshots
^^^^^^^^^^^

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot1.png

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot2.png

Tiles
^^^^^

If collective.cover is installed, two new tiles will be available: Facebook and Twitter.

The Facebook tile embeds a Facebook Page.
You can set the width and height, and you can control some other aspects of the widget.
A Facebook application ID must be defined in the Social Like configlet in order to use this tile.
Instructions for obtaining a Facebook application ID can be found at `Facebook's developer site <https://developers.facebook.com/docs/apps#register>`_

The Twitter tile embeds a Twitter timeline.
Timelines are an easy way to embed multiple tweets on your website in a compact, single-column view.
You can set the width, height and tweet limit, and you can use a widget ID.
A Twitter username must be defined in the Social Like configlet in order to use this tile.

.. figure:: https://github.com/collective/sc.social.like/raw/master/docs/tiles.png
    :align: center
    :height: 600px
    :width: 800px

    The Twitter and Facebook tiles.

TODO:

* [ ] Facebook: return a comma-separated string of tabs to render
* [ ] Twitter: allow to remove a display component of a timeline (chrome)
* [ ] Twitter: refresh the tile after editing it
* [ ] RobotFramework tests for both tiles
* [ ] Plone 5.1 compatibility
