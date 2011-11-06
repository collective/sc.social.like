===============================================
Social: Like Actions (sc.social.like)
===============================================

.. contents:: Table of Contents
   :depth: 2


Overview
--------

**Social: Like Actions** is a Plone package (add-on) providing simple Google+,
Twitter and Facebook integration for Plone Content Types.

This package installs a viewlet with actions to +1, Tweet and Like (or
Recommend) a content.

Requirements
------------

    - Plone 4.1.x (http://plone.org/products/plone)
    - Plone 4.0.x (http://plone.org/products/plone)
    - Plone 3.3.x (http://plone.org/products/plone)

Screenshot
-----------

    .. image:: https://bitbucket.org/simplesconsultoria/sc.social.like/raw/e95bc09f7337/docs/screenshot.png

Installation
------------

To enable this product, on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.social.like``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.social.like

.. note:: Since Plone 3.3 is not is necessary to explictly inform 
          plone.recipe.zope2instance recipe to install the ZCML slug

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Using in a Plone Site
----------------------

Step 1: Activate it
^^^^^^^^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **Social: Like Actions** (check checkbox at its left side)
and click the 'Activate' button.

Step 2: Configure it
^^^^^^^^^^^^^^^^^^^^^^

Go to the 'Site Setup' page in the Plone interface and click on the
'Social Like' link -- under Add-on Configuration.

.. image:: https://bitbucket.org/simplesconsultoria/sc.social.like/raw/e95bc09f7337/docs/control_panel.png

There you can configure how **Social: Like Actions** will behave, which actions
will be displayed and for which content types.

Uninstall
-------------

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product **Social: Like Actions**, which should be under *Activated
add-ons*, (check checkbox at its left side) and click the 'Deactivate' button.

.. note:: You may have to empty your browser cache and save your resource 
          registries in order to see the effects of the product installation.

Contributing
--------------

    Code repository and isssue tracker can be found at 
    `BitBucket <https://bitbucket.org/simplesconsultoria/sc.social.like>`_

Sponsoring
----------

Development of this product was sponsored by :
    
    * `Rede Brasil Atual <http://www.redebrasilatual.com.br/>`_
    
    * `TV1 <http://www.grupotv1.com.br/>`_
    
    * `Brazilian Government <http://www.planalto.gov.br/>`_

Credits
-------
    
    * Cleber Santos (cleber at simplesconsultoria dot com dot br) - Idea and 
      implementation.
    
    * Andre Nogueira (andre at simplesconsultoria dot com dot br) - CSS magic

    * Hector Velarde (hvelarde at simplesconsultoria dot com dot br) - Fixes

