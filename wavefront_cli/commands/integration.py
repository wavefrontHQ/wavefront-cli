
from wavefront_cli.lib import message
from wavefront_cli.lib import util

from wavefront_cli.integrations.teststatsd import TestStatsD

from json import dumps

from .base import Base

import importlib


class Integration(Base):

    def run(self):

        message.print_welcome()
        print 'Hello, world!'
        print 'You supplied the following options:', dumps(self.options, indent=2, sort_keys=True)


        int_name = self.options['<name>']
        int_install = self.options['install']
        int_options = self.options['<option>']
        int_options = util.options_to_dict(int_options)


        message.print_bold(int_name + " Integration")
        message.print_bold("Options:")
        for k,v in int_options.iteritems():
            message.print_bold(k + ": " + v)



        integration_class = getattr(importlib.import_module("wavefront_cli.integrations"), int_name)
        instance = integration_class(int_options)
        instance.install_config()
        instance.install_dashboard()

        # Testing StatsD class
        #statsd_integration = TestStatsD(statsd_port=8125)
        #statsd_integration.install_config()
