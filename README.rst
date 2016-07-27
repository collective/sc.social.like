=====================================
Social: Like Actions (sc.social.like)
=====================================

.. contents:: Table of Contents
   :depth: 2


Life, the Universe, and Everything
----------------------------------

This package provides integration for the following social networks in Plone:

* Facebook
* Google+
* LinkedIn
* Pinterest
* Telegram
* Twitter
* WhatsApp (mobile only)

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

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/control_panel.png

There you can configure how **Social: Like Actions** will behave, which actions
will be displayed and for which content types.

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

Screenshots
^^^^^^^^^^^

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot1.png

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot2.png
