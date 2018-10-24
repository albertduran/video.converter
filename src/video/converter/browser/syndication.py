from Products.CMFPlone.browser.syndication.adapters import DexterityItem
from Products.CMFPlone.interfaces.syndication import IFeed
from zope.component import adapts
from video.converter.interfaces import IVideoEnabled
from zope.cachedescriptors.property import Lazy as lazy_property


class VideoFeedItem(DexterityItem):
    adapts(IVideoEnabled, IFeed)

    @property
    def file_url(self):
        url = self.base_url

        fi = self.file
        if fi is not None:
            filename = fi.filename
            if filename:
                url += '/@@download/video_file/%s' % filename
        return url

    @property
    def has_enclosure(self):
        if self.context.video_file:
            return True
        return False

    @lazy_property
    def file(self):
        if self.has_enclosure:
            return self.context.video_file
