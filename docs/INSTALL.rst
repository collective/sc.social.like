Installation
------------

To enable this product in a buildout-based installation:

1. Edit your buildout.cfg and add ``sc.social.like`` to the list of eggs to
   install::

    [buildout]
    ...
    eggs =
        sc.social.like

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``sc.social.like`` and click the 'Activate' button.

Note: You may have to empty your browser cache and save your resource
registries in order to see the effects of the product installation.
