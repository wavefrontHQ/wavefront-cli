"""Initialize wavefront cli version."""

import pkg_resources

__version__ = None

try:
    __version__ = pkg_resources.get_distribution('wavefront-cli').version
except pkg_resources.DistributionNotFound:
    # __version__ is only available when the distribution is installed.
    pass
