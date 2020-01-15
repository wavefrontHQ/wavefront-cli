"""Blueprint for managing integrations."""

import subprocess

from ..lib import message


class Base:
    """base integration class."""

    def __init__(self, name, options):
        """Prepare the system for installing the integration."""
        self.name = name
        self.options = options

        cmd = "mkdir -p /etc/telegraf/telegraf.d"
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            message.print_warn("Unable to create integrations config directory"
                               " at /etc/telegraf/telegraf.d")

    def validate_options(self):
        """Blueprint to validate integration options."""
        raise NotImplementedError('You must implement the validate_options()'
                                  ' method!')

    def install(self):
        """Blueprint to install integration."""
        raise NotImplementedError('You must implement the install() method!')

    def remove(self):
        """Blueprint to remove integration."""
        raise NotImplementedError("You must implement the remove() method!")

    def print_success(self):
        """Notify for successful installation."""
        message.print_success("Successfully installed %s integration!"
                              % self.name)

    def print_failure(self):
        """Notify for failed installation."""
        message.print_warn("Failed to install %s integration!" % self.name)
