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

Screenshot
^^^^^^^^^^

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/screenshot.png

Don't Panic
-----------

Step 1: Activate it
^^^^^^^^^^^^^^^^^^^

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

Step 2: Configure it
^^^^^^^^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Social Like' link -- under Add-on Configuration.

.. image:: https://github.com/collective/sc.social.like/raw/master/docs/control_panel.png

There you can configure how **Social: Like Actions** will behave, which actions
will be displayed and for which content types.

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/sc.social.like.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/sc.social.like

.. image:: https://coveralls.io/repos/collective/sc.social.like/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/sc.social.like

.. image:: https://pypip.in/d/sc.social.like/badge.png
    :target: https://pypi.python.org/pypi/sc.social.like/
    :alt: Downloads

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/sc.social.like/issues
