from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapts
from zope.interface import implements
from video.converter.interfaces import (
    IMediaEnabled, IVideoEnabled
)
from video.converter.behavior import IVideo


class PrimaryFieldInfo(object):
    implements(IPrimaryFieldInfo)
    adapts(IMediaEnabled)

    def __init__(self, context):
        self.context = context
        if IVideoEnabled.providedBy(self.context):
            self.fieldname = 'video_file'
            self.field = IVideo[self.fieldname]

    @property
    def value(self):
        return self.field.get(self.context)
