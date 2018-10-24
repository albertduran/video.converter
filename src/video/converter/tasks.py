from collective.celery import task
from video.converter import convert


@task.as_admin()
def convertVideoFormats(context):
    convert.convertVideoFormats(context)
