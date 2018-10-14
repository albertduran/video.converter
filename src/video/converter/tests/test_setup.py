# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from video.converter.testing import VIDEO_CONVERTER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that video.converter is properly installed."""

    layer = VIDEO_CONVERTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if video.converter is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'video.converter'))

    def test_browserlayer(self):
        """Test that IVideoConverterLayer is registered."""
        from video.converter.interfaces import (
            IVideoConverterLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IVideoConverterLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = VIDEO_CONVERTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['video.converter'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if video.converter is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'video.converter'))

    def test_browserlayer_removed(self):
        """Test that IVideoConverterLayer is removed."""
        from video.converter.interfaces import \
            IVideoConverterLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IVideoConverterLayer,
            utils.registered_layers())
