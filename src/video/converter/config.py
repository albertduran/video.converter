class Format(object):

    def __init__(self, name, extension, type_, quality):
        """Inicialitation of format."""
        self.name = name
        self.extension = extension
        self.type_ = type_
        self.quality = quality


CONVERTABLE_FORMATS = [
    Format('OGG(360p)', 'ogv', 'ogg_360', '640x360'),
    Format('WebM(360p)', 'webm', 'webm_360', '640x360'),
    Format('OGG(480p)', 'ogv', 'ogg_480', '854x480'),
    Format('WebM(480p)', 'webm', 'webm_480', '854x480'),
    Format('OGG(720p)', 'ogv', 'ogg_720', '1280x720'),
    Format('WebM(720p)', 'webm', 'webm_720', '1280x720')]


def getFormat(type_):
    """Get available formats to convert video."""
    for tt in CONVERTABLE_FORMATS:
        if tt.type_ == type_:
            return tt
