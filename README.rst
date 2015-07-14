=====================================
Social: Like Actions (sc.social.like)
=====================================

.. contents:: Table of Contents
   :depth: 2


Life, the Universe, and Everything
----------------------------------

**Social: Like Actions** is a Plone package (add-on) providing simple social
networks integration for Plone Content Types.

This package ships with plugins for the following networks:

* Facebook
* Google+
* LinkedIn
* Pinterest
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

.. Note::
    You may have to empty your browser cache and save your resource registries
    in order to see the effects of the product installation.

Configuration
^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Social Like' link -- under Add-on Configuration.

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/control_panel.png

There you can configure how **Social: Like Actions** will behave, which actions
will be displayed and for which content types.

Privacy and cookies
^^^^^^^^^^^^^^^^^^^

Social networks and privacy togheter is a thorny argument, let say that
social media widget commonly tracks user actions and add 3rd party cookies.

If privacy is something you must care about (for example: if you need to take
care of the `European Cookie Law`_) sc.social.like provide a
"*Do not track users*" option.
When enabled, social media widget are rendered as simple HTML links at the expense
of features and user experience.

This product is also respecting the `Do Not Track`_ browser user's preference.
If the user configured his browser for beeing not tracked, social media will
be rendered as the "*Severe privacy*" settings is enabled.

Screenshots
^^^^^^^^^^^

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot1.png

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot2.png

.. _`European Cookie Law`: http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:32009L0136
.. _`Do Not Track`: http://donottrack.us/
