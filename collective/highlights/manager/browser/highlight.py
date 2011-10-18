from zope import component, interface
from z3c.form import form, field, button
from z3c.form.interfaces import HIDDEN_MODE
from plone.z3cform.templates import ViewPageTemplateFile
# from plone.memoize.view import memoize_contextless
from Products.Five.browser import BrowserView

from collective.highlights.manager import MessageFactory as _
from collective.highlights.manager.interfaces import IHighlighted
from collective.highlights.manager.interfaces import IHighlightDataStorage
from collective.highlights.manager.interfaces import IHighlightGroupSelect
from collective.highlights.manager.util import getHliteTool, getActiveUser


def getDefaultGroup(context):
    hlite = getHliteTool()
    return hlite.getGroupsFor(context)[0]


class GroupSelectForm(form.Form):

    label = _(u"Select Group")
    fields = field.Fields(IHighlightGroupSelect).omit('selected_group')
    ignoreContext = True

    def __init__(self, *args):
        form.Form.__init__(self, *args)
        self.group = None

    def update(self):
        form.Form.update(self)
        if 'group' in self.request:
            self.widgets['group'].value = self.request['group']

    @button.buttonAndHandler(_('Select Group'), name='selgroup')
    def handleSelect(self, action):
        data, errors = self.extractData()
        self.group = data['group']
        self.status = _(u'Group selected')
        self.updateWidgets()


class EditHighlight(form.EditForm):

    edit_label = _(u"Edit Highlight Data")
    add_label = _(u"Highlight Data")

    description = _(u"Highlight data that will appear in any configured highlight UI")
    template = ViewPageTemplateFile('templates/edithighlight.pt')
    ignoreRequest = True

    def __init__(self, *args):
        form.EditForm.__init__(self, *args)
        self.hlite = getHliteTool()
        self.highlights = IHighlightDataStorage(self.context)
        self.group_obj = None

    @property
    def label(self):
        if self.isEditing():
            return self.edit_label
        else:
            return self.add_label

    @property
    def fields(self):
        schema = self.group_obj.schema
        fields = (field.Fields(schema) +
            field.Fields(IHighlightGroupSelect).select('selected_group'))
        fields['selected_group'].ignoreContext = True
        return fields

    @property
    def ignoreContext(self):
        return not (self.group_obj and self.group_obj.id in self.highlights)

    def getContent(self):
        content = self.highlights.get(self.group_obj.id, None)
        if content is None:
            content = self.getDefaultContent()
        return content

    def getDefaultContent(self):
        for name, factory in component.getFactoriesFor(self.group_obj.schema):
            if name == 'highlightdata':
                return factory()

    def update(self):
        self.groupsel = GroupSelectForm(self.context, self.request)
        self.groupsel.update()
        if self.groupsel.group is None:
            group = self.request.get('group', None)
            if group and group in self.highlights:
                self.group_obj = self.hlite[group]
            else:
                self.group_obj = getDefaultGroup(self.context)
        else:
            self.group_obj = self.groupsel.group
        super(EditHighlight, self).update()

    def updateWidgets(self):
        form.EditForm.updateWidgets(self)
        if self.group_obj:
            self.widgets['selected_group'].value = self.group_obj.id
        self.widgets['selected_group'].mode = HIDDEN_MODE

    def isEditing(self):
        """Returns True if context is highlighted in group"""

        return self.group_obj and self.group_obj.id in self.highlights or False

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if data['selected_group']:
            self.group_obj = self.hlite[data['selected_group']]
            content = self.getContent()
            del data['selected_group']
            changes = form.applyChanges(self, content, data)
            if self.group_obj.id not in self.highlights:
                self.highlights[self.group_obj.id] = content
                interface.alsoProvides(self.context, IHighlighted)
            if changes:
                content.author = getActiveUser()
                self.context.reindexObject(idxs=['object_provides',
                                                 'hlite_groups'])
                self.status = self.successMessage
                self.refreshActions = True
                self.updateWidgets()
            else:
                self.status = self.noChangesMessage
        else:
            self.status = _(u'Please select a group.')

    @button.buttonAndHandler(_(u'Delete'), name='delete',
                             condition=lambda form: form.isEditing())
    def handleDelete(self, action):
        data, errors = self.extractData()
        if data['selected_group']:
            self.group_obj = self.hlite[data['selected_group']]
            self.group_obj.removeItem(obj=self.context)
            self.updateWidgets()
            self.status = self.successMessage
            self.refreshActions = True
        else:
            self.status = _(u'Please select a group.')


class TestHighlightable(BrowserView):

    def __call__(self):
        return self.hlite_tool().enabledFor(self.context)

#    @memoize_contextless
    def hlite_tool(self):
        print __file__, self.__class__.__name__, 'hlite_tool'
        return getHliteTool()
