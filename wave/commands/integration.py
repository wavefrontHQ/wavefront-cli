"""The integration command."""


from json import dumps

from .base import Base


class Integration(Base):
    """Install a Wavefront Integration."""

    def run(self):
        print 'Hello from integrations'
        print 'Running integration installer with the following options:', dumps(self.options, indent=2, sort_keys=True)
        
