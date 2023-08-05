"""discogs-api init.py"""

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "0.0.2"

from discogs_api.client import Client
from discogs_api.models import (
    Artist,
    Release,
    Master,
    Label,
    User,
    Listing,
    Track,
    Price,
    Video,
)
