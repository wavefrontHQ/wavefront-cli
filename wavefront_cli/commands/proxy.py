"""The proxy command."""
from json import dumps
from .base import Base
# wavefront API functions
from wavefront.api import validate_token, clean_url
import wavefront.auth
import wavefront.system
import wavefront.proxy

import subprocess
import json
import os
import sys
import platform

class Proxy(Base):
    """Install the Wavefront Proxy."""

    def run(self):

        print 'Running proxy installer'

        if self.options['remove']:
            #self.uninstall_proxy()
            wavefront.system.remove_service("wavefront-proxy")
            sys.exit(0)
        elif self.options['install']:
            creds = wavefront.auth.get_or_set_auth(self.options)
            if creds == None:
                print "Unable to obtain Wavefront API credentials."
                sys.exit(0)

            wf_url = creds['user_url']
            api_token = creds['user_token']

            # 1) Run packagecloud installation
            print "Running proxy installation"
            #self.install_proxy()
            wavefront.proxy.install_proxy()

            # 2) Configure proxy
            print "Configuring proxy"
            #self.configure_proxy(wf_url,api_token)
            wavefront.proxy.configure_proxy(wf_url,api_token)

        else:
            print 'You must pass either the "install" or "remove" flag to the proxy command. Run "wave -h" for more information.'
