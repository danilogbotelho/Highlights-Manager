from zope.i18nmessageid import MessageFactory
from Products.CMFCore.utils import ToolInit


MessageFactory = MessageFactory('collective.highlights.manager')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from collective.highlights.manager import tool
    ToolInit(tool.HighlightsTool.meta_type,
             tools=(tool.HighlightsTool,),
             icon=tool.HighlightsTool.toolicon).initialize(context)
