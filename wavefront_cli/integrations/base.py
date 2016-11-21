

class Base(object):
    """A base command."""

    def __init__(self, options):
        self.options = options

    def install(self):
        raise NotImplementedError('You must implement the install() method!')

    def remove(self):
        raise NotImplementedError("YOu must implement the remove() method!")

