import subprocess
from wavefront_cli.lib import auth
from wavefront_cli.lib import message

class Base(object):
    """base integration class."""

    def __init__(self, name, options):

        self.name = name
        self.options = options

        cmd = "mkdir -p /etc/telegraf/telegraf.d"
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            message.print_warn("Unable to create integrations config directory at /etc/telegraf/telegraf.d")


    def validate_options(self):
        raise NotImplementedError('You must implement the validate_options() method!')

    def install(self):
        raise NotImplementedError('You must implement the install() method!')

    def remove(self):
        raise NotImplementedError("You must implement the remove() method!")

    def print_success(self):
        message.print_success("Successfully installed %s integration!" % (self.name))

    def print_failure(self):
        message.print_warn("Failed to install %s integration!" % (self.name))
