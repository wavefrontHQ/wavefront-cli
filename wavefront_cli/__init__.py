"""Initialize wavefront cli version."""

import importlib.metadata

__version__ = None

try:
    __version__ = importlib.metadata.version('wavefront-cli')
except importlib.metadata.PackageNotFoundError:
    # __version__ is only available when the distribution is installed.
    pass
