from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from OFS.ObjectManager import IFAwareObjectManager
from OFS.OrderedFolder import OrderedFolder
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager

from zope import interface
from zope.schema.fieldproperty import FieldProperty
from zope.app.component.hooks import getSite

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBaseTool import PloneBaseTool

from collective.highlights.manager import interfaces as ifaces
from collective.highlights.manager.config import HLITE_TOOL_ID
from collective.highlights.manager.config import HLITE_GROUP_META
from collective.highlights.manager.config import HLITE_TOOL_META


class HighlightsGroup(PropertyManager, SimpleItem):
    """ A group for highlightable items."""

    interface.implements(ifaces.IHighlightsGroup)

    security = ClassSecurityInfo()

    manage_options = (
        ({'label': 'Edit', 'action': 'zmi_edit'},)
        + PropertyManager.manage_options
        + SimpleItem.manage_options)

    meta_type = HLITE_GROUP_META

    name = FieldProperty(ifaces.IHighlightsGroup['name'])
    title = FieldProperty(ifaces.IHighlightsGroup['title'])
    description = FieldProperty(ifaces.IHighlightsGroup['description'])
    type_filter_enabled = FieldProperty(ifaces.IHighlightsGroup['type_filter_enabled'])
    types_whitelist = FieldProperty(ifaces.IHighlightsGroup['types_whitelist'])
    schema = FieldProperty(ifaces.IHighlightsGroup['schema'])

    @property
    def id(self):
        return self.name

    def _setId(self, newid):
        self.name = newid

    def __init__(self, name, title=u'', description=u'',
                 type_filter_enabled=False, types_whitelist=None, schema=None):
        super(HighlightsGroup, self).__init__()
        self.name = name
        self.title = title
        self.description = description
        self.type_filter_enabled = type_filter_enabled
        if types_whitelist is not None:
            self.types_whitelist = types_whitelist
        self.schema = schema

    @property
    def context(self):
        return getToolByName(getSite(), HLITE_TOOL_ID)

    def __repr__(self):
        return u"<%s('%s')>" % (self.__class__.__name__, self.name)

    def getContentItems(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['object_provides'] = ifaces.IHighlighted.__identifier__
        query['hlite_groups'] = self.id
        brains = portal_catalog(**query)
        for brain in brains:
            yield brain

    def getItems(self):
        for content in self.getContentItems():
            yield ifaces.IHighlightDataStorage(content.getObject())[self.id]

    def removeItem(self, uid=None, obj=None):
        assert (uid and not obj) or (not uid and obj), "removeItem either by uid or by obj instance"
        if not obj:
            portal_catalog = getToolByName(self.context, 'portal_catalog')
            brains = portal_catalog(UID=uid)
            obj = brains[0].getObject()

        highlights = ifaces.IHighlightDataStorage(obj)
        del highlights[self.id]
        idxs = ['hlite_groups']
        if len(highlights) == 0:
            interface.noLongerProvides(obj, ifaces.IHighlighted)
            idxs.append('object_provides')
        obj.reindexObject(idxs=idxs)

InitializeClass(HighlightsGroup)


class HighlightsTool(PloneBaseTool, UniqueObject, IFAwareObjectManager,
                     OrderedFolder, PropertyManager):
    """ """
    try:
        __implements__ = (PloneBaseTool.__implements__,
                      OrderedFolder.__implements__,
                      SimpleItem.__implements__, )
    except AttributeError:
        pass

    interface.implements(ifaces.IHighlightsTool)

    security = ClassSecurityInfo()

    id = HLITE_TOOL_ID
    title = "Highlights Manager"
    meta_type = HLITE_TOOL_META
    toolicon = 'browser/resources/hlitestool_icon.gif'
    _product_interfaces = (ifaces.IHighlightsGroup,)

    manage_options = (OrderedFolder.manage_options)

    @property
    def context(self):
        return self.__parent__

    def addGroup(self, group):
        if not ifaces.IHighlightsGroup.providedBy(group):
            group = HighlightsGroup(**group)
        self._setObject(group.id, group)

    def deleteGroup(self, group):
        #TODO: remove highlighted data
        self._delObject(group)

    def deleteGroups(self, groups):
        for group in groups:
            self.deleteGroup(group)

    def getAllGroups(self):
        return self.objectItems(HLITE_GROUP_META)

    def enabledFor(self, context):
        """Checks whether the context object is allowed to be highlighted"""
        for gr_id, gr in self.getAllGroups():
            if not gr.type_filter_enabled:
                return True
            else:
                if context.portal_type in gr.types_whitelist:
                    return True
        return False

    def getGroupsFor(self, context):
        """Gets groups the context object is allowed to be highlighted in"""

        groups = []
        for gr_id, gr in self.getAllGroups():
            if not gr.type_filter_enabled:
                groups.append(gr)
            else:
                if context.portal_type in gr.types_whitelist:
                    groups.append(gr)
        return groups

    def getAllHighlights(self):
        """Returns and iterator over all the highlights in the site"""

        portal_catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['object_provides'] = ifaces.IHighlighted.__identifier__
        brains = portal_catalog(**query)
        for brain in brains:
            hlite_brain = ifaces.IHighlightDataStorage(brain.getObject())
            yield hlite_brain

    def getHighlights(self, group):
        """Returns an iterator over the highlights registered under group."""

        return self[group].getItems()

InitializeClass(HighlightsTool)
