from .base import *  # NOQA

try:
    from .production_settings import *  # NOQA
except ImportError:
    pass

try:
    from .local_settings import *  # NOQA
except ImportError:
    pass
