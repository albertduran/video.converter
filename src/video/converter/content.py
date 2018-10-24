from video.converter.interfaces import IVideoEnabled
from plone.dexterity.content import Item
from zope.interface import implements


class Video(Item):
    implements(IVideoEnabled)
