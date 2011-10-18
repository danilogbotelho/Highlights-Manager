from zope import interface
from zope.component import getUtilitiesFor
from zope.component.interfaces import IFactory
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from collective.highlights.manager.interfaces import IHighlightSchema
from collective.highlights.manager.util import getHliteTool


class GroupSchemaVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        for (name, factory) in getUtilitiesFor(IFactory):
            if name == 'highlightdata':
                interfaces = factory.getInterfaces()
                if len(list(interfaces)) > 1:
                    for iface in interfaces:
                        if iface.isOrExtends(IHighlightSchema):
                            schema = iface
                            break
                else:
                    schema = interfaces[0]
                terms.append(SimpleVocabulary.createTerm(schema, str(schema),
                                                         factory.title))
        return SimpleVocabulary(terms)


class GroupsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        self.hlite = getHliteTool()
        terms = []
        for group in self.hlite.getGroupsFor(context):
            terms.append(SimpleVocabulary.createTerm(group, group.id,
                                                     group.title))
        return SimpleVocabulary(terms)
