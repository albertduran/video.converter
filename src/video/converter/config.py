class Format(object):

    def __init__(self, name, extension, type_, quality):
        """Inicialitation of format."""
        self.name = name
        self.extension = extension
        self.type_ = type_
        self.quality = quality


CONVERTABLE_FORMATS = [
    Format('MP4(240p)', 'mp4', 'mp4_240', '426x240'),
    Format('WebM(240p)', 'webm', 'webm_240', '426x240'),
    Format('MP4(360p)', 'mp4', 'mp4_360', '640x360'),
    Format('WebM(360p)', 'webm', 'webm_360', '640x360'),
    Format('MP4(480p)', 'mp4', 'mp4_480', '854x480'),
    Format('WebM(480p)', 'webm', 'webm_480', '854x480'),
    Format('MP4(720p)', 'mp4', 'mp4_720', '1280x720'),
    Format('WebM(720p)', 'webm', 'webm_720', '1280x720'),
    Format('MP4(1080p)', 'mp4', 'mp4_1080', '1920x1080'),
    Format('WebM(1080p)', 'webm', 'webm_1080', '1920x1080')]


def getFormat(type_):
    """Get available formats to convert video."""
    for tt in CONVERTABLE_FORMATS:
        if tt.type_ == type_:
            return tt
