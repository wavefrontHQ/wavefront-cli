"""The proxy command."""


from json import dumps

from .base import Base


class Proxy(Base):
    """Install the Wavefront Proxy."""

    def run(self):
        print 'Hello from proxy'
        print 'Running proxy installer with the following options:', dumps(self.options, indent=2, sort_keys=True)
