from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

class Fixture(PloneSandboxLayer):
    
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.highlights.manager
        self.loadZCML(package=collective.highlights.manager)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.highlights.manager:default')

FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.highlights.manager:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='collective.highlights.manager:Functional')
