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
        "avconv_in_webm", "avconv_out_webm",
        "avconv_in_ogg", "avconv_out_ogg")


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


from plone.batching import Batch
order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5}


class VideoCourseView(BrowserView):
    """ Filtered content search view for every folder. """

    def update(self):
        self.query = self.request.form.get('q', '')
        if self.request.form.get('t', ''):
            self.tags = [v for v in self.request.form.get('t').split(',')]
        else:
            self.tags = []

    def get_batched_contenttags(self, query=None, batch=True, b_size=10, b_start=0):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)
        r_results = pc.searchResults(path=path,
                                     sort_on='sortable_title',
                                     sort_order='ascending')

        items_favorites = self.marca_favoritos(r_results)
        #items_nofavorites = self.exclude_favoritos(r_results)

        items = self.ordenar_results(items_favorites, [])

        batch = Batch(items, b_size, b_start)
        return batch

    def get_contenttags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query and not self.tags:
            return self.getContent()

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query) + '*'

            if self.tags:
                r_results = pc.searchResults(path=path,
                                             SearchableText=query,
                                             Subject={'query': self.tags, 'operator': 'and'},
                                             sort_on='sortable_title',
                                             sort_order='ascending')
            else:
                r_results = pc.searchResults(path=path,
                                             SearchableText=query,
                                             sort_on='sortable_title',
                                             sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items
        else:
            r_results = pc.searchResults(path=path,
                                         Subject={'query': self.tags, 'operator': 'and'},
                                         sort_on='sortable_title',
                                         sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items

    def get_tags_by_query(self):
        pc = getToolByName(self.context, "portal_catalog")

        def quotestring(s):
            return '"%s"' % s

        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if not self.query == '':
            multispace = u'\u3000'.encode('utf-8')
            for char in ('?', '-', '+', '*', multispace):
                self.query = self.query.replace(char, ' ')

            query = self.query.split()
            query = " AND ".join(query)
            query = quote_bad_chars(query)
            path = self.context.absolute_url_path()

            r_results = pc.searchResults(path=path,
                                         Subject=query,
                                         sort_on='sortable_title',
                                         sort_order='ascending')

            items_favorites = self.marca_favoritos(r_results)
            items_nofavorites = self.exclude_favoritos(r_results)

            items = self.ordenar_results(items_favorites, items_nofavorites)

            return items
        else:
            return self.get_batched_contenttags(query=None, batch=True, b_size=10, b_start=0)

    def get_container_path(self):
        return self.context.absolute_url()

    def getContent(self):
        portal = api.portal.get()
        catalog = getToolByName(portal, 'portal_catalog')
        path = self.context.getPhysicalPath()
        path = "/".join(path)

        r_results_parent = catalog.searchResults(path={'query': path, 'depth': 1},
                                                 sort_on='sortable_title',
                                                 sort_order='ascending')

        items_favorites = self.favorites_items(path)
        items_nofavorites = self.exclude_favoritos(r_results_parent)

        items = self.ordenar_results(items_favorites, items_nofavorites)

        return items

    def ordenar_results(self, items_favorites, items_nofavorites):
        """ Ordena los resultados segun el tipo (portal_type)
            segun este orden: (order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5})
            y devuelve el diccionario con los favoritos y no favoritos. """
        items_favorites_by_tipus = sorted(items_favorites, key=lambda item: item['tipus'])
        items_nofavorites_by_tipus = sorted(items_nofavorites, key=lambda item: item['tipus'])

        items = [dict(favorite=items_favorites_by_tipus,
                      nofavorite=items_nofavorites_by_tipus)]
        return items

    def marca_favoritos(self, r_results):
        """ De los resultados obtenidos devuelve una lista con los que son FAVORITOS y le asigna un valor al tipus
            segun este orden: (order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5}) """
        current_user = api.user.get_current().id
        favorite = []
        favorite = [{'obj': r, 'tipus': order_by_type[r.portal_type] if r.portal_type in order_by_type else 6}
                    for r in r_results if current_user in r.favoritedBy]

        return favorite

    def favorites_items(self, path):
        """ Devuelve todos los favoritos del usuario y le asigna un valor al tipus
            segun este orden: (order_by_type = {"Folder": 1, "Document": 2, "File": 3, "Link": 4, "Image": 5}) """
        pc = api.portal.get_tool(name='portal_catalog')
        current_user = api.user.get_current().id
        results = pc.searchResults(path={'query': path},
                                   favoritedBy=current_user,
                                   sort_on='sortable_title',
                                   sort_order='ascending')

        favorite = [{'obj': r, 'tipus': order_by_type[r.portal_type]
                     if r.portal_type in order_by_type else 6} for r in results]
        return favorite
