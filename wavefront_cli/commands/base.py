"""The Blueprint for all the command."""


class Base:  # pylint: disable=too-few-public-methods
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
