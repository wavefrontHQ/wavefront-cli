
from wavefront_cli.lib import message
from wavefront_cli.lib import util
from wavefront_cli.lib import system

from json import dumps
import importlib
import sys
from .base import Base



class Integration(Base):

    def run(self):

        message.print_welcome()

        int_name = self.options['<name>']
        int_options = self.options['<option>']
        int_options = util.option_to_dict(int_options)


        message.print_bold(int_name + " Integration with Options:")
        for k,v in int_options.iteritems():
            print k,": ",v


        integration_class = None
        try:
            integration_class = getattr(importlib.import_module("wavefront_cli.integrations"), int_name)
            instance = integration_class(int_name, int_options)
        except:
            message.print_warn("Error: Unrecognized Integration: " + int_name)
            sys.exit(1)


        if self.options['install']:
            print "Action: install"
            if not instance.install():
                instance.print_failure()
                sys.exit(1)
            else:
                instance.print_success()

        elif self.options['remove']:
            print "Action: remove"
            if not instance.remove():
                instance.print_failure()
                sys.exit(1)
            else:
                instance.print_success()

        system.restart_service("telegraf")
        sys.exit(0)