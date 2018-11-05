# -*- coding: utf-8 -*-
import json
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from video.converter import _
from video.converter.browser.widget import StreamNamedFileFieldWidget
from video.converter.settings import GlobalSettings
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import alsoProvides, implements
from zope.interface import Invalid


def valid_video(namedblob):
    if namedblob.contentType.split('/')[0] != 'video':
        raise Invalid("must be a video file")
    return True


def getDefaultWidth():
    portal = getSite()
    settings = GlobalSettings(portal)
    return settings.default_video_width


def getDefaultHeight():
    portal = getSite()
    settings = GlobalSettings(portal)
    return settings.default_video_height


class IVideo(model.Schema):

    form.omitted('image')
    image = namedfile.NamedBlobImage(
        title=_(u"Cover Image"),
        description=u"",
        required=False,
    )

    # main file will always be converted to mp4
    form.widget(video_file=StreamNamedFileFieldWidget)
    model.primary('video_file')
    video_file = namedfile.NamedBlobFile(
        title=_(u"Video File"),
        description=u"",
        required=False,
        constraint=valid_video
    )

    form.omitted(IAddForm, 'webm_240')
    form.omitted(IEditForm, 'webm_240')
    form.widget(webm_240=StreamNamedFileFieldWidget)
    webm_240 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'webm_360')
    form.omitted(IEditForm, 'webm_360')
    form.widget(webm_360=StreamNamedFileFieldWidget)
    webm_360 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'webm_480')
    form.omitted(IEditForm, 'webm_480')
    form.widget(webm_480=StreamNamedFileFieldWidget)
    webm_480 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'webm_720')
    form.omitted(IEditForm, 'webm_720')
    form.widget(webm_720=StreamNamedFileFieldWidget)
    webm_720 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'webm_1080')
    form.omitted(IEditForm, 'webm_1080')
    form.widget(webm_1080=StreamNamedFileFieldWidget)
    webm_1080 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'mp4_240')
    form.omitted(IEditForm, 'mp4_240')
    form.widget(mp4_240=StreamNamedFileFieldWidget)
    mp4_240 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'mp4_360')
    form.omitted(IEditForm, 'mp4_360')
    form.widget(mp4_360=StreamNamedFileFieldWidget)
    mp4_360 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'mp4_480')
    form.omitted(IEditForm, 'mp4_480')
    form.widget(mp4_480=StreamNamedFileFieldWidget)
    mp4_480 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'mp4_720')
    form.omitted(IEditForm, 'mp4_720')
    form.widget(mp4_720=StreamNamedFileFieldWidget)
    mp4_720 = namedfile.NamedBlobFile(
        required=False,
    )

    form.omitted(IAddForm, 'mp4_1080')
    form.omitted(IEditForm, 'mp4_1080')
    form.widget(mp4_1080=StreamNamedFileFieldWidget)
    mp4_1080 = namedfile.NamedBlobFile(
        required=False,
    )

    width = schema.Int(
        title=_(u"Width"),
        defaultFactory=getDefaultWidth
    )

    height = schema.Int(
        title=_(u"Height"),
        defaultFactory=getDefaultHeight
    )

    form.omitted('metadata')
    metadata = schema.Text(
        required=False
    )


alsoProvides(IVideo, IFormFieldProvider)


class UnsettableProperty(object):
    """
    Property that can not be saved from a form
    """

    def __init__(self, field):
        self._field = field

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return getattr(inst.context, self._field.__name__, self._field.default)

    def __set__(self, inst, value):
        pass

    def __getattr__(self, name):
        return getattr(self._field, name)


class BasicProperty(object):

    def __init__(self, field):
        self._field = field

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return getattr(inst.context, self._field.__name__, self._field.default)

    def __set__(self, inst, value):
        setattr(inst.context, self._field.__name__, value)

    def __getattr__(self, name):
        return getattr(self._field, name)


class BaseAdapter(object):

    def _get_metadata(self):
        return unicode(json.dumps(getattr(self.context, 'metadata', {})))

    def _set_metadata(self, value):
        pass

    metadata = property(_get_metadata, _set_metadata)


_marker = object()


class Video(BaseAdapter):
    implements(IVideo)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    # For when a fileUpload sends us a file
    def _get_file(self):
        return self.context.video_file

    def _set_file(self, value):
        self.video_file = value
    file = property(_get_file, _set_file)

    def _get_video_file(self):
        return self.context.video_file

    def _set_video_file(self, value):
        if value is None:
            self.context.video_file = None
        elif value != getattr(self.context, 'video_file', _marker):
            self.context.video_converted = False
            self.context.video_file = value

    video_file = property(_get_video_file, _set_video_file)
    image = BasicProperty(IVideo['image'])
    width = BasicProperty(IVideo['width'])
    height = BasicProperty(IVideo['height'])
    webm_240 = UnsettableProperty(IVideo['webm_240'])
    webm_360 = UnsettableProperty(IVideo['webm_360'])
    webm_480 = UnsettableProperty(IVideo['webm_480'])
    webm_720 = UnsettableProperty(IVideo['webm_720'])
    webm_1080 = UnsettableProperty(IVideo['webm_1080'])
    mp4_240 = UnsettableProperty(IVideo['mp4_240'])
    mp4_360 = UnsettableProperty(IVideo['mp4_360'])
    mp4_480 = UnsettableProperty(IVideo['mp4_480'])
    mp4_720 = UnsettableProperty(IVideo['mp4_720'])
    mp4_1080 = UnsettableProperty(IVideo['mp4_1080'])
    image = UnsettableProperty(IVideo['image'])
