"""The ec2-tag command."""


from json import dumps

from .base import Base


class Proxy(Base):
    """Install Wavefront AWS utils."""

    def run(self):
        print 'Hello from AWS utils'
        print 'Running AWS utils with the following options:', dumps(self.options, indent=2, sort_keys=True)
