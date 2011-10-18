from zope import interface, component
from zope.annotation.interfaces import IAnnotations
from plone.indexer.decorator import indexer

from collective.highlights.manager.interfaces import IHighlightable
from collective.highlights.manager.interfaces import IHighlightDataStorage
from collective.highlights.manager.interfaces import IHighlighted
from collective.highlights.manager.storage import HighlightData
from collective.highlights.manager.storage import HighlightDataStorage
from collective.highlights.manager.config import HLITE_ANNO_KEY
from collective.highlights.manager import MessageFactory as _


HighlightDataFactory = component.factory.Factory(HighlightData,
                                          _('Default HighlightData Factory'))


@component.adapter(IHighlightable)
@interface.implementer(IHighlightDataStorage)
def getHighlightDataStorage(context):
    annotations = IAnnotations(context)
    mapping = annotations.get(HLITE_ANNO_KEY, None)
    if mapping is None:
        mapping = annotations[HLITE_ANNO_KEY] = HighlightDataStorage()
    return mapping


@indexer(IHighlighted)
def hlite_groups(object):
    return IHighlightDataStorage(object).keys()
