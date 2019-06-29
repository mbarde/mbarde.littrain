# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import mbarde.littrain


class MbardeLittrainLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=mbarde.littrain)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mbarde.littrain:default')


MBARDE_LITTRAIN_FIXTURE = MbardeLittrainLayer()


MBARDE_LITTRAIN_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MBARDE_LITTRAIN_FIXTURE,),
    name='MbardeLittrainLayer:IntegrationTesting',
)


MBARDE_LITTRAIN_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MBARDE_LITTRAIN_FIXTURE,),
    name='MbardeLittrainLayer:FunctionalTesting',
)


MBARDE_LITTRAIN_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MBARDE_LITTRAIN_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='MbardeLittrainLayer:AcceptanceTesting',
)
