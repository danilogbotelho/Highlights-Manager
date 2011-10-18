from zope import interface
from zope.schema.fieldproperty import FieldProperty
from zope.location.interfaces import ILocation
from zope.app.container.btree import BTreeContainer
from zope.annotation.interfaces import IAttributeAnnotatable

from collective.highlights.manager.interfaces import IHighlightDefaultSchema
from collective.highlights.manager.interfaces import IHighlightData
from collective.highlights.manager.interfaces import IHighlightDataStorage


class HighlightDataStorage(BTreeContainer):
    interface.implements(IHighlightDataStorage)


class HighlightDataBase(BTreeContainer):
    """
    >>> data = HighlightData()

    Simple values saved as object attributes

    >>> data['attr1'] = 'value1'
    >>> data['attr1']
    'value1'

    >>> data.get('attr1')
    'value1'

    >>> getattr(data, 'attr1')
    'value1'

    >>> 'attr1' in data
    False

    >>> del data['attr1']

    >>> getattr(data, 'attr1', None) is None
    True

    >>> data['attr1']
    Traceback (most recent call last):
    ...
    KeyError: 'attr1'


    Locatable objects saved as container items

    >>> class Test(object):
    ...     interface.implements(ILocation)
    ...     __parent__ = __name__ = None

    >>> data['attr2'] = Test()

    >>> data['attr2']
    <collective.highlights.manager.storage.Test ...>

    >>> data.get('attr2')
    <collective.highlights.manager.storage.Test ...>

    >>> hasattr(data, 'attr2')
    False

    >>> 'attr2' in data
    True

    >>> data['attr2'].__parent__ is data
    True

    >>> del data['attr2']

    >>> 'attr2' in data
    False

    >>> data['attr2']
    Traceback (most recent call last):
    ...
    KeyError: 'attr2'


    """

    interface.implements(IHighlightData, IAttributeAnnotatable)

    def get(self, name, default=None):
        if name in self:
            return super(HighlightData, self).__getitem__(name)

        elif hasattr(self, name):
            return getattr(self, name, default)

        else:
            return default

    def __getitem__(self, name):
        if name in self:
            return super(HighlightData, self).__getitem__(name)

        elif hasattr(self, name):
            return getattr(self, name)

        raise KeyError(name)

    def __setitem__(self, name, value):
        if ILocation.providedBy(value):
            super(HighlightData, self).__setitem__(name, value)

            if hasattr(self, name):
                delattr(self, name)

        else:
            setattr(self, name, value)

    def __delitem__(self, name):
        if name in self:
            super(HighlightData, self).__delitem__(name)

        if hasattr(self, name):
            delattr(self, name)


class HighlightData(HighlightDataBase):

    interface.implements(IHighlightDefaultSchema)

    title = FieldProperty(IHighlightDefaultSchema['title'])
    btitle = FieldProperty(IHighlightDefaultSchema['btitle'])
    description = FieldProperty(IHighlightDefaultSchema['description'])
    bdescription = FieldProperty(IHighlightDefaultSchema['bdescription'])
    if 'image' in IHighlightDefaultSchema:
        image = FieldProperty(IHighlightDefaultSchema['image'])
