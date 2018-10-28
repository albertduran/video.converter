# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles

# http://developer.plone.org/security/custom_permissions.html
security = ModuleSecurityInfo('plone.app.contenttypes')
TYPE_ROLES = ('Manager', 'Site Administrator', 'Owner', 'Editor')

security.declarePublic('video.converter.AddVideo')
setDefaultRoles('video.converter.AddVideo', TYPE_ROLES)
AddVideo = "video.converter.AddVideo"
