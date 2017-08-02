Changelog
---------

There's a frood who really knows where his towel is.

2.10.1 (2017-08-02)
^^^^^^^^^^^^^^^^^^^

- Fix ``data-href`` attribute on Facebook plugin to point to canonical URL;
  this should finally fix the counter on the widget.
  [rodfersou]

- Fix Canonical URL updater form;
  a new upgrade step is provided to update the ``objects_provides`` catalog index (fixes `#115 <https://github.com/collective/sc.social.like/issues/115>`_).
  [hvelarde]

- Add ``canonical_domain`` field record to the registry when upgrading;
  this fixes an issue in the upgrade step to profile version 3045 (fixes `#114 <https://github.com/collective/sc.social.like/issues/114>`_).
  [hvelarde]


2.10 (2017-07-17)
^^^^^^^^^^^^^^^^^

- Fix support for canonical URL in Facebook's Open Graph for Dexterity-based content types;
  previously the current URL was incorrectly used as the canonical URL of an item leading to zeroed counters when moving content around or when changing the schema to access the site (HTTP to HTTPS).
  Check package documentation for more information on how to use this new feature (fixes `#104 <https://github.com/collective/sc.social.like/issues/104>`_).
  [hvelarde]

- Drop support for Plone 4.2.
  [rodfersou]

- In Plone 5, keep in sync some redundant fields found in the new Social Media configlet.
  Changes on ``facebook_app_id``, ``facebook_username``, or ``twitter_username`` fields will be reflected in both configlets (fixes `#100`_).
  [hvelarde]


2.9 (2017-03-09)
^^^^^^^^^^^^^^^^^^

- Add Facebook control panel setting for showing/hiding the number of likes. By
  default the Facebook plugin still shows the likes.
  [fredvd]


2.8b1 (2017-02-03)
^^^^^^^^^^^^^^^^^^

- Update Brazilian Portuguese and Spanish translations.
  [hvelarde]

- Add support to share content by email (closes `#91`_).
  [rodfersou, hvelarde]


2.7b1 (2017-01-09)
^^^^^^^^^^^^^^^^^^^

- Add missing upgrade step to cook CSS resources.
  [hvelarde]

- Don't fail in the Twitter plugin if the title has non-ASCII characters.
  [csenger, hvelarde]

- Add metadata for Twitter Cards (closes `#65`_).
  [rodfersou]


2.6b1 (2016-12-21)
^^^^^^^^^^^^^^^^^^

- Code clean up; tests related with loading BMP images were removed as make no sense.
  [hvelarde]

- Do not show social like viewlet for unpublished content (closes `#83`_).
  [rodfersou]

- Fix package dependencies.
  [maurits, hvelarde]


2.6a1 (2016-09-23)
^^^^^^^^^^^^^^^^^^

- Add Facebook and Twitter tiles for collective.cover.
  The Facebook tile embeds a Facebook Page.
  The Twitter tile embeds a Twitter timeline.
  [hvelarde]

- Add `title` attributes to Telegram and WhatsApp share links.
  [hvelarde]

- Enforce constraints on `enabled_portal_types` field to avoid `WrongType` error while running upgrade step to v3040.
  [hvelarde]

- Do not fail on adding Facebook's 'Like' button while running upgrade step to v3010.
  [fredvd, hvelarde]


2.5 (2016-07-26)
^^^^^^^^^^^^^^^^^^

- Added Telegram plugin (closes `#52`_).
  [rodfersou]

- Use Plone's registry instead of the ``portal_properties`` tool to store package configuration (closes `#1`_).
  [hvelarde]


2.4.1 (2015-12-10)
^^^^^^^^^^^^^^^^^^

- Update package classifiers; Plone 5 was included by mistake in the list of supported versions.
  [hvelarde]

- Use "application/javascript" media type instead of the obsolete "text/javascript".
  [hvelarde]


2.4 (2015-09-17)
^^^^^^^^^^^^^^^^

- Drop explicit support for Plone 4.1 and Python 2.6;
  package should work, but we are not testing anymore with those versions so compatibility is not guaranteed.
  [hvelarde]

- Fix caching issues with WhatsApp button by moving mobile detection client-side (closes `#56`_).
  [rodfersou]

- Add Dutch translations.
  [fredvd]

- Fix uninstall error.
  [bsuttor]


2.3 (2015-07-14)
^^^^^^^^^^^^^^^^

- Added the "Do not track users" configuration option, to prevent social
  networks from sending cookies to site's visitors.
  This will replace social badges with simple links.
  [keul]

- Added German translations.
  [tohafi]


2.2 (2015-05-04)
^^^^^^^^^^^^^^^^

- Added WhatsApp plugin (closes `#39`_).
  [rodfersou]


2.1 (2015-03-02)
^^^^^^^^^^^^^^^^

- Translations to Brazilian Portuguese and Spanish were updated.
  [hvelarde]

- Removed deprecated portal_actionicons registration
  [keul]

- Translation fixes: some label were not translated
  [keul]

- Facebook "Share" button now provided. See `#15`_.
  [keul]

- Added missing migration step for refreshing CSS registry
  [keul]


2.0.2 (2015-02-23)
^^^^^^^^^^^^^^^^^^

- Removed old Facebook specific CSS rule that truncate the new Facebook widget. This close `#38`_.
  [keul]


2.0.1 (2015-02-23)
^^^^^^^^^^^^^^^^^^

- Nothing changed (brown bag release).


2.0 (2015-02-10)
^^^^^^^^^^^^^^^^

- Do not load social media stuff on non-canonical views (like edit form or similar). This close `#36`_.
  [keul]

- Added italian translation.
  [keul]

- Load behavior of all social plugins changed to be async.
  [keul]

- Fixed a problem with images loaded in news. If the image isn't a JPG,
  the `get_content_image` method can't get image size and returns nothing.
  This avoid some strange things, like MemoryError with Pillow.
  [cekk]

- If a field named "image" isn't an ImageField, do not break the viewlet.
  [cekk]

- Add exception handling also for TypeError in get_content_image method.
  [cekk]

- Fixed metadata og:type, used value 'article' for internal page.
  [fdelia]


2.0rc1 (2014-10-14)
^^^^^^^^^^^^^^^^^^^

- Use safe_unicode to deal with accented chars in content Title.
  [ericof]


2.0b4 (2014-08-08)
^^^^^^^^^^^^^^^^^^

- Fixed styling for action buttons. Now they are displayed side by side
  [agnogueira]

- Fix an UnicodeDecodeError in the Twitter plugin (Reported by Programa Interlegis)
  [ericof]


2.0b3 (2014-06-06)
^^^^^^^^^^^^^^^^^^

- Fix a division by zero issue happening with AT Images during creation (while on portal_factory)
  [ericof]


2.0b2 (2014-06-02)
^^^^^^^^^^^^^^^^^^

- Facebook now recommends 1200 x 630 images
  [ericof]


2.0b1 (2014-02-07)
^^^^^^^^^^^^^^^^^^^^

- Use View permission on viewlets to avoid security failures into viewlet
  if anonymous try to display non public parts of site.
  [thomasdesvenain]

- Fix package dependencies.
  [hvelarde]


2.0a2 (2013-11-04)
^^^^^^^^^^^^^^^^^^^^

- Use content language instead of request language, avoiding cache problems
  https://github.com/collective/sc.social.like/issues/19
  [ericof]


2.0a1 (2013-07-23)
^^^^^^^^^^^^^^^^^^^^

- Drop support for Plone 4.0.x [ericof]

- Increasing test coverage [ericof]

- Render metadata viewlet on folder_full_view and all_content templates
  https://github.com/collective/sc.social.like/issues/11 [ericof]

- Fixes vertical display
  https://github.com/collective/sc.social.like/issues/5 [ericof]

- Add LinkedIn and Pinterest support.
  https://github.com/collective/sc.social.like/issues/6 [ericof]

- Plugin implementation [ericof]

- Ensure all resources are loaded using scheme-relative URLs.  Previously,
  attempting to load off HTTP on HTTPS sites resulted in broken pages.
  [davidjb]

- Plone 3.x is not officially supported anymore; use it at your own risk.
  [hvelarde]

- Change CSS import to link.
  [agnogueira]


Previous entries can be found in the HISTORY.rst file.

.. _`#1`: https://github.com/collective/sc.social.like/issues/1
.. _`#15`: https://github.com/collective/sc.social.like/pull/15
.. _`#36`: https://github.com/collective/sc.social.like/issues/36
.. _`#38`: https://github.com/collective/sc.social.like/issues/38
.. _`#39`: https://github.com/collective/sc.social.like/issues/39
.. _`#52`: https://github.com/collective/sc.social.like/issues/52
.. _`#56`: https://github.com/collective/sc.social.like/issues/56
.. _`#65`: https://github.com/collective/sc.social.like/issues/65
.. _`#83`: https://github.com/collective/sc.social.like/issues/83
.. _`#91`: https://github.com/collective/sc.social.like/issues/91
.. _`#100`: https://github.com/collective/sc.social.like/issues/100
