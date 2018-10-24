# -*- coding: utf-8 -*-
from video.converter.async import convertVideoFormats


def video_added(video, event):
    if getattr(video, 'video_file', None):
        convertVideoFormats(video)


def video_edited(video, event):
    if getattr(video, 'video_file', None):
        convertVideoFormats(video)
