import urllib

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as pmf
from Products.Five import BrowserView
from plone import api
from plone.app.z3cform.layout import wrap_form
from plone.memoize.instance import memoize
from video.converter import _
from video.converter.config import getFormat
from video.converter.interfaces import IGlobalMediaSettings
from video.converter.interfaces import IMediaEnabled
from video.converter.settings import GlobalSettings
from video.converter.subscribers import video_edited
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form import group
from zope.component.hooks import getSite

try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    from zope.interface import Interface as IDisableCSRFProtection  # noqa


class VideoView(BrowserView):

    def get_edit_url(self):
        """
        If the user can edit the video, returns the edit url.
        """
        if not api.user.has_permission(
            'Modify portal content',
                obj=self.context):
            return ""
        from plone.protect.utils import addTokenToUrl
        url = "%s/@@edit" % self.context.absolute_url()
        return addTokenToUrl(url)


class DefaultGroup(group.Group):
    label = u"Default"
    fields = field.Fields(IGlobalMediaSettings).select(
        "additional_video_formats", "async_quota_size",
        "default_video_width", "default_video_height")


class ConversionSettingsGroup(group.Group):
    label = u"Conversion settings"
    fields = field.Fields(IGlobalMediaSettings).select(
        "avconv_in_mp4", "avconv_out_mp4",
        "avconv_in_webm", "avconv_out_webm")


class GlobalSettingsForm(group.GroupForm, form.EditForm):
    groups = (DefaultGroup, ConversionSettingsGroup)

    label = _(u"Media Settings")
    description = _(u'description_media_global_settings_form',
                    default=u"Configure the parameters for media.")

    @button.buttonAndHandler(pmf('Save'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)

        self.status = pmf('Changes saved.')


GlobalSettingsFormView = wrap_form(GlobalSettingsForm)


class ConvertVideo(BrowserView):
    def __call__(self):
        # Mark the video as not converted
        self.context.video_converted = False
        video_edited(self.context, None)
        self.request.response.redirect(self.context.absolute_url())


class Utils(BrowserView):

    def valid_type(self):
        return IMediaEnabled.providedBy(self.context)

    @memoize
    def settings(self):
        return GlobalSettings(getSite())

    @property
    @memoize
    def base_wurl(self):
        base_url = self.context.absolute_url()
        return base_url + '/@@view/++widget++form.widgets.'

    @property
    @memoize
    def base_furl(self):
        return self.base_wurl + 'IVideo.'

    @memoize
    def videos(self):
        types = []
        # Problema con los types si no tenemos el src porque no se ha convertido el video todavia
        settings = GlobalSettings(
            getToolByName(self.context, 'portal_url').getPortalObject())
        for type_ in settings.additional_video_formats:
            format = getFormat(type_)
            if format:
                types.append((format.extension, format.type_, format.quality))
        videos = []
        for (extension, file_id, resolution) in types:
            file = getattr(self.context, file_id, None)
            if file:
                videos.append({
                    'type': extension,
                    'url': self.base_furl + file_id + '/@@stream',
                    'quality': resolution.split('x')[1]
                })
        return videos

    @memoize
    def mp4_url(self):
        videos = self.videos()
        if videos:
            return videos[0]['url']
        else:
            return None

    @memoize
    def image_url(self):
        image = getattr(self.context, 'image', None)
        if image:
            return '%s/@@images/image' % (
                self.context.absolute_url()
            )
        else:
            return None

    @memoize
    def mp4_url_quoted(self):
        url = self.mp4_url()
        if url:
            return urllib.quote_plus(url)
        else:
            return url

    @memoize
    def image_url_quoted(self):
        url = self.image_url()
        if url:
            return urllib.quote_plus(url)
        else:
            return url
