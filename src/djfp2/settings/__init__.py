from .base import *  # NOQA

try:
    from .production_settings import *  # NOQA
except ImportError:
    pass
