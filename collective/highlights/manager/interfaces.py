from zope.interface import Interface
from zope import schema
try:
    from plone.namedfile import field
except ImportError:
    field = None

from collective.highlights.manager import MessageFactory as _


class IHighlightable(Interface):
    """Marker interface for content that can be highlighted """


class IHighlighted(Interface):
    """Marker interface for content that is highlighted"""


class IHighlightSchema(Interface):
    """ """


class IHighlightDefaultSchema(IHighlightSchema):
    """Highlight data"""

    title = schema.TextLine(
        title=_(u'Highlight Title'),
        description=_(u'A short text for this content in its highlight view.'),
        required=False)

    btitle = schema.Bool(
        title=_(u"Bind to content's title"),
        description=_(u"If marked, will use the content's title."),
        required=False)

    description = schema.Text(
        title=_(u'Highlight Description'),
        description=_(u'A longer text for this content in its highlight view.'),
        required=False)

    bdescription = schema.Bool(
        title=_(u"Bind to content's description"),
        description=_(u"If marked, will use the content's description."),
        required=False)

    if field:
        image = field.NamedImage(
            title=_(u"Image"),
            required=False)


class IHighlightData(Interface):
    """ """


class IHighlightDataStorage(Interface):
    """ """


class IHighlightDataFactory(Interface):
    """ """


class IHighlightGroupSelect(Interface):
    group = schema.Choice(title=_(u"Group"), required=True,
                          vocabulary="collective.highlights.manager.Groups")

    selected_group = schema.ASCIILine(__name__='selected_group',
                                      required=False)


class IHighlightsGroup(Interface):
    """Represents a group of highlighted items."""

    name = schema.ASCIILine(
        title=_(u"Name"),
        description=_(u"A unique identifier for the group. Can not be changed after creation."),
        required=True)

    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"A user readable short description."),
        required=True)

    description = schema.Text(
        title=_(u"Description"),
        description=_(u"A user readable longer description."),
        required=False,
        default=u'')

    type_filter_enabled = schema.Bool(
        title=_(u"Enable Content Type Filtering"),
        description=_(u"If enabled, only content types in the below whitelist will be highlightable."),
        required=False,
        default=False)

    types_whitelist = schema.Tuple(
        title=_(u"Allowed Content Types"),
        required=False,
        default=tuple(),
        value_type=schema.Choice(
           vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"))

    schema = schema.Choice(
        title=_(u"Data schema"),
        required=True,
        description=_(u"Can only be changed if there are no items in group."),
        vocabulary="collective.highlights.manager.GroupSchemas")


class IHighlightsTool(Interface):
    groups = schema.List(
        title=_(u"Groups"),
        description=_(u"A list of groups highlighted content might be enrolled in."),
        value_type=schema.Object(IHighlightsGroup, title=_(u"Group")),
        required=False)
