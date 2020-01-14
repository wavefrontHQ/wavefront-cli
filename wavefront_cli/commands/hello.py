"""The hello command."""
# pylint: disable=R0903

from __future__ import print_function

from json import dumps

from .base import Base


class Hello(Base):
    """Say hello, world."""

    def run(self):
        """Say hello, world to test the run method."""
        print('Hello, world!')
        print('You supplied the following options:',
              dumps(self.options, indent=2, sort_keys=True))
