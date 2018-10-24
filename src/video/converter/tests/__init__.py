import os
from plone.namedfile import NamedBlobFile
from shutil import copyfile
from tempfile import mktemp

current_dir = os.path.abspath(os.path.dirname(__file__))
test_file_dir = os.path.join(current_dir, 'files')


def _getBlob(_type='video', _format='mp3'):
    filename = u'test.%s' % _format

    newpath = mktemp()
    origpath = os.path.join(test_file_dir, filename)
    copyfile(origpath, newpath)
    fi = open(newpath)
    blob = NamedBlobFile(fi, filename=filename)
    fi.close()
    return blob


def getVideoBlob(_format='mp4'):
    return _getBlob('video', _format)
