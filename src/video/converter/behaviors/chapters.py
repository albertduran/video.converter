# -*- coding: utf-8 -*-
"""
Module for add IChapter behavior to Folders to be able to choose Subjects.

And show it as <h2>Title</h2> in video_course_view.
"""

from video.converter import _
from zope import schema
from zope.interface import implements
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider
from plone import api
import unicodedata
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IContextSourceBinder
from zope.interface import directlyProvides


def subjectInTerms(terms, subject):
    """Return True if subject in terms else False."""
    for term in terms:
        if subject == term.title:
            return True
    return False


def tagsInContext(context):
    """Vocabulary for show Subjects in IChapter behavior."""
    terms = []
    literals = api.content.find(portal_type="Video", context=context)
    for item in literals:
        for s in item.Subject:
            if not subjectInTerms(terms, s):
                flattened = unicodedata.normalize('NFKD', s.decode(
                    'utf-8')).encode('ascii', errors='ignore')
                terms.append(SimpleVocabulary.createTerm(s, flattened, s))
    return SimpleVocabulary(terms)


directlyProvides(tagsInContext, IContextSourceBinder)


@provider(IFormFieldProvider)
class IChapter(model.Schema):
    """Behavior interface to be able to choose Subjects as themes of course."""

    additional_chapters = schema.List(
        title=_("Chapters in this course"),
        description=_('additional_chapters_help'),
        required=False,
        value_type=schema.Choice(source=tagsInContext))


class Chapter(object):
    """Implements IChapter interface."""

    implements(IChapter)

    def __init__(self, context):
        """Initialize IChapter behavior."""
        self.context = context

    def _set_additional_chapters(self, value):
        self.context.additional_chapters = value

    def _get_additional_chapters(self):
        return getattr(self.context, 'additional_chapters',
                       self.context.additional_chapters)

    additional_chapters = property(_get_additional_chapters,
                                   _set_additional_chapters)
