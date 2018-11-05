try:
    import collective.celery  # noqa
    from video.converter import tasks
except ImportError:
    tasks = None

from video.converter import pasync
from video.converter import convert
from plone import api
from zope.globalrequest import getRequest


def _run(obj, func):
    # return func(obj)
    if tasks:
        # collective.celery is installed
        tfunc = getattr(tasks, func.__name__)
        tfunc.delay(obj)
    elif pasync.asyncInstalled():
        # plone.app.async installed
        pasync.queueJob(obj, func)
    else:
        func(obj)


def convertVideoFormats(video):
    api.portal.show_message(
        'Converting video to compatible formats. Be patient.',
        request=getRequest())
    _run(video, convert.convertVideoFormats)
