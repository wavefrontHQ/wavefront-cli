

class Base(object):
    """A base command."""

    def __init__(self, options):
        self.options = options

    def install_config(self):
        raise NotImplementedError('You must implement the install_config() method!')

    def install_dashboard(self):
        raise NotImplementedError('You must implement the install_dashboard() method!')

