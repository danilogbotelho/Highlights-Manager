from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from collective.highlights.manager.tool import HLITE_TOOL_ID


# Get the portal object without context/request
def getPortal():
    return getUtility(ISiteRoot)


def getHliteTool():
    return getPortal()[HLITE_TOOL_ID]


def getActiveUser():
    mt = getToolByName(getPortal(), 'portal_membership')
    if mt.isAnonymousUser():
        return None
    else:
        member = mt.getAuthenticatedMember()
        username = member.getUserName()
        return username
