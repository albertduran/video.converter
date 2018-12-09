# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Products.Five import BrowserView
from video.converter.interfaces import IVideoEnabled
from plone.memoize.instance import memoize
from Products.CMFPlone import PloneMessageFactory as pmf


class VideoCourseView(BrowserView):
    """ Listing view for video courses. """

    @property
    def b_size(self):
        b_size = getattr(self.request, 'b_size', None)\
            or getattr(self.request, 'limit_display', None) or 20
        return int(b_size)

    @property
    def b_start(self):
        b_start = getattr(self.request, 'b_start', None) or 0
        return int(b_start)

    @property
    @memoize
    def course_titles(self):
        """Get all title from Subjects of videos in this folder."""
        return self.context.additional_chapters

    @property
    @memoize
    def course_number_videos(self):
        """Get number of videos from this folder."""
        videos = self.results(
            batch=False,
            object_provides=IVideoEnabled.__identifier__,
        )
        return len(videos)

    @property
    def no_items_message(self):
        return pmf(
            'description_no_videos_in_folder',
            default=u'There are currently no videos in this folder.'
        )

    @property
    def no_subjects_message(self):
        return pmf(
            'description_no_subjects_configured',
            default=u'There are currently no subjects configured to show videos\
                      or videos in this folder are not categorized.'
        )

    @property
    def text(self):
        textfield = getattr(aq_base(self.context), 'text', None)
        text = textfield.output_relative_to(self.context)\
            if getattr(textfield, 'output_relative_to', None)\
            else None
        if text:
            self.text_class = 'stx' if textfield.mimeType in (
                'text/structured', 'text/x-rst', 'text/restructured'
            ) else 'plain'
        return text

    def results(self, **kwargs):
        """Return a content listing based result set with contents of the
        folder.

        :param **kwargs: Any keyword argument, which can be used for catalog
                         queries.
        :type  **kwargs: keyword argument

        :returns: plone.app.contentlisting based result set.
        :rtype: ``plone.app.contentlisting.interfaces.IContentListing`` based
                sequence.
        """
        # Extra filter
        kwargs.update(self.request.get('contentFilter', {}))
        if 'object_provides' not in kwargs:  # object_provides is more specific
            kwargs.setdefault('portal_type', self.friendly_types)
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        listing = aq_inner(self.context).restrictedTraverse(
            '@@folderListing', None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results

    def course_videos(self, subject):
        """Get all videos categorized with subject from this folder."""
        videos = self.results(
            batch=False,
            object_provides=IVideoEnabled.__identifier__,
            Subject=subject,
            sort_on='getObjPositionInParent',
        )
        return videos
