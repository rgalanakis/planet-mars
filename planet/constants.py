__version__ = "3.0"
__url__ = 'https://github.com/rgalanakis/planet-mars'


# Useful common date/time formats
TIMEFMT_ISO = "%Y-%m-%dT%H:%M:%S+00:00"
TIMEFMT_822 = "%a, %d %b %Y %H:%M:%S +0000"


# Version information (for generator headers)
VERSION = ("Planet/%s +http://www.planetplanet.org" % __version__)

REQUIRED_OPTIONS = (
    'name',
    'link',
    'feed',
    'owner_name',
    'owner_email',
    'feed_timeout',
    'template_files',
    'date_format'
)
