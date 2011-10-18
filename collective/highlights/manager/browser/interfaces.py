from zope.interface import Interface


class IProductSpecific(Interface):
    """A layer specific for this product.

    We will use this to register browser pages that should only be used
    when this product is installed in the site.
    """
