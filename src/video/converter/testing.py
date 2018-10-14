# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import video.converter


class VideoConverterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=video.converter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'video.converter:default')


VIDEO_CONVERTER_FIXTURE = VideoConverterLayer()


VIDEO_CONVERTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VIDEO_CONVERTER_FIXTURE,),
    name='VideoConverterLayer:IntegrationTesting',
)


VIDEO_CONVERTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VIDEO_CONVERTER_FIXTURE,),
    name='VideoConverterLayer:FunctionalTesting',
)


VIDEO_CONVERTER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        VIDEO_CONVERTER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='VideoConverterLayer:AcceptanceTesting',
)
