from zope.interface import Interface, implements
from zope.component import adapts
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form import form, field, button
from z3c.form.interfaces import DISPLAY_MODE
from plone.app.z3cform.layout import wrap_form

from plone.z3cform.crud import crud
from plone.app.z3cform import layout

from Products.ATContentTypes.interfaces.interfaces import IATContentType

from collective.highlights.manager import interfaces as ifaces
from collective.highlights.manager import MessageFactory as _
from collective.highlights.manager.util import getHliteTool
from collective.highlights.manager.browser.groups_overview import back_to_highlightsmanager


class uwAddGroupForm(form.Form):
    fields = field.Fields(ifaces.IHighlightsGroup)
    ignoreContext = True  # don't use context to get widget data
    label = _(u"Add Highlights Group")

    def __init__(self, *args, **kwargs):
        super(uwAddGroupForm, self).__init__(*args, **kwargs)
        self.hlite = getHliteTool()

    @button.buttonAndHandler(_(u'Add'))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return
        self.hlite.addGroup(data)
        self.context.plone_utils.addPortalMessage(_('Group successfully added.'))
        self.request.RESPONSE.redirect(self.context.absolute_url())
AddGroupForm = wrap_form(uwAddGroupForm, back_link=back_to_highlightsmanager)


# TODO: when changing content type whitelist, if highlighted content exists
# either remove them or disallow the change
class uwEditGroupForm(form.EditForm):
    fields = field.Fields(ifaces.IHighlightsGroup).omit('name')
    label = _(u"Edit Highlights Group")

    def updateWidgets(self):
        form.EditForm.updateWidgets(self)
        for dummy in self.context.getContentItems():
            self.widgets['schema'].mode = DISPLAY_MODE
            break
EditGroupForm = wrap_form(uwEditGroupForm, back_link=back_to_highlightsmanager)


class IGroupMember(Interface):
    title = schema.TextLine(title=_(u"Title"))
    author = schema.Text(title=_(u"Highlight Author"))


class GroupMember(object):
    implements(IGroupMember)
    adapts(IATContentType)

    def __init__(self, member, group):
        highlight = ifaces.IHighlightDataStorage(member.getObject())[group]
        self.title = unicode(member.Title) or unicode(member.id)
        self.author = highlight.author
        self.url = member.getURL()


class GroupMembersEditForm(crud.EditForm):
    label = _(u"Highlighted items")


class GroupMembersForm(crud.CrudForm):
    """View list of items assigned to a group and allows for deletion"""

    addform_factory = crud.NullForm
    editform_factory = GroupMembersEditForm
    view_schema = IGroupMember

    def get_items(self):
        group = self.context.id
        return [(hl.UID, GroupMember(hl, group)) for hl in
                self.context.getContentItems()]

    def remove(self, (id, item)):
        self.context.removeItem(id)

    def link(self, item, field):
        if field == 'title':
            return item.url + '/@@highlight?group=%s' % self.context.id

GroupMembers = layout.wrap_form(
    GroupMembersForm,
    index=ViewPageTemplateFile('templates/form_layout.pt'),
    label=_(u"Group members"),
    back_link=back_to_highlightsmanager)
