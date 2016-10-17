"""The proxy command."""


from json import dumps

from .base import Base


class Agent(Base):
    """Install the Wavefront Proxy."""

    def run(self):
        print 'Hello from agent'
        print 'Running agent installer with the following options:', dumps(self.options, indent=2, sort_keys=True)
