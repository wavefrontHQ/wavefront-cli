"""The Blueprint for all the command."""

# pylint: disable=C,R


class Base:
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """Prepare for a command."""
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Needs to be implemented for all the commands."""
        raise NotImplementedError('You must implement the run()'
                                  ' method yourself!')
