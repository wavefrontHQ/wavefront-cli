"""The agent command.
wave agent [--proxy-address=<address>] [--proxy-port=<port>]
"""

import platform
import sys
import subprocess
from .base import Base
import wavefront.system
import wavefront.agent


class Agent(Base):
    """Install the Wavefront Agent."""
    def run(self):

        if self.options['install']:
            proxy_info = wavefront.agent.input_proxy_info(self.options)
            #self.install_agent()
            wavefront.agent.install_agent()
            #self.configure_agent(proxy_info)
            wavefront.agent.configure_agent(proxy_info)
            print "Agent installation finished"
        elif self.options['remove']:
            wavefront.system.remove_service("telegraf")
            print "Agent uninstall finished"




