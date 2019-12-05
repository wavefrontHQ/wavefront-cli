"""Manage Integration command."""

# pylint: disable=R0903

from __future__ import print_function

import importlib
import sys

from wavefront_cli.lib import message
from wavefront_cli.lib import system
from wavefront_cli.lib import util


from .base import Base


class Integration(Base):
    """Manage Integrations."""

    def run(self):
        """Install/Remove Integrations."""
        message.print_welcome()

        int_name = self.options['<name>']
        int_options = self.options['<option>']
        int_options = util.option_to_dict(int_options)

        message.print_bold(int_name + " Integration with Options:")
        for key, value in int_options.items():
            print(key, ": ", value)

        integration_class = None
        try:
            integration_class = getattr(importlib.import_module(
                "wavefront_cli.integrations"), int_name)
            instance = integration_class(int_name, int_options)
        except AttributeError:
            message.print_warn("Error: Unrecognized Integration: " + int_name)
            sys.exit(1)

        if self.options['install']:
            print("Action: install")
            if not instance.install():
                instance.print_failure()
                sys.exit(1)
            else:
                instance.print_success()

        elif self.options['remove']:
            print("Action: remove")
            if not instance.remove():
                instance.print_failure()
                sys.exit(1)
            else:
                instance.print_success()

        system.restart_service("telegraf")
        sys.exit(0)
