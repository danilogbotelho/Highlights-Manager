from zope.interface import Interface, implements
from zope.component import adapts
from zope import schema
from zope.app.component.hooks import getSite
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.app.pagetemplate import viewpagetemplatefile
from z3c.form import button
from z3c.form import field
from plone.app.z3cform import layout
from plone.z3cform import z2
from plone.z3cform.crud import crud
from Products.CMFCore.utils import getToolByName

from collective.highlights.manager.interfaces import IHighlightsGroup
from collective.highlights.manager import MessageFactory as _

def back_to_controlpanel(self):
    root = getSite()
    return dict(label=_(u"Up to Site Setup"),
                url=root.absolute_url() + '/plone_control_panel')

def back_to_highlightsmanager(self):
    root = getSite()
    return dict(label=_(u"Up to Highlights Manager Configuration"),
                url=root.absolute_url() + '/highlights_manager')

class IGroupOverview(Interface):
    title = schema.TextLine(title=_(u"Title"))
    description = schema.Text(title=_(u"Description"))

class GroupOverview(object):
    implements(IGroupOverview)
    adapts(IHighlightsGroup)

    def __init__(self, group):
        self.group = group
        self.group_id = group.id
        self.title = group.title
        self.description = group.description

class EditForm(crud.EditForm):
    
    label = ''
    
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.highlights_manager = getToolByName(self.context, 'highlights_manager')
        
    @button.buttonAndHandler(_('Delete'), name='delete')
    def handle_delete(self, action):
        self.status = _(u"Please select items to remove.")
        selected = self.selected_items()
        if selected:
            self.status = _(u"Successfully removed categories.")
            self.highlights_manager.deleteGroups([id for id, gr_o in selected])

class GroupOverviewForm(crud.CrudForm):
    """View list of groups and allow for deletion and addition."""
    
    addform_factory = crud.NullForm
    editform_factory = EditForm
    view_schema = IGroupOverview

    def __init__(self, *args, **kwargs):
        super(GroupOverviewForm, self).__init__(*args, **kwargs)
        self.highlights_manager = getToolByName(self.context, 'highlights_manager')
        
    def get_items(self):
        return [(group_id, GroupOverview(group))
                for group_id, group in self.highlights_manager.getAllGroups()]

    def remove(self, (id, item)):
        self.highlights_manager.deleteGroups([id])
    
    def link(self, item, field):
        if field == 'title':
            return '%s/edit' % item.group.absolute_url()

GroupsOverview = layout.wrap_form(
    GroupOverviewForm,
    index=ViewPageTemplateFile('templates/controlpanel.pt'),
    label = _(u"Highlights Manager: Groups Overview"),
    back_link=back_to_controlpanel)