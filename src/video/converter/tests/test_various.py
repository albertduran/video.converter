# -*- coding: utf-8 -*-
import unittest2 as unittest
import os

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from video.converter.testing import (
    MEDIA_FUNCTIONAL_TESTING
)

from video.converter.settings import GlobalSettings


class TestVarious(unittest.TestCase):

    layer = MEDIA_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        settings = GlobalSettings(self.portal)
        settings.additional_video_formats = []
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_controlpanel(self):
        self.browser.open(self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.browser.getLink('Media Settings').click()
        self.assertTrue('webm' in self.browser.contents)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
