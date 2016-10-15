"""The proxy command."""
from json import dumps
from .base import Base
import requests
import subprocess
import json
import os
import sys
import platform

class Proxy(Base):
    """Install the Wavefront Proxy."""

    pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
    pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"


    def check_os(self):
        try:
            if platform.linux_distribution() == ('', '', ''):
                #aws linux workaround
                return platform.linux_distribution(supported_dists=['system'])[0]
            else:
                return platform.linux_distribution[0]
        except:
            print "Unable to detect Linux distribution. ", sys.exc_info()



    def run(self):
        print 'Hello from proxy'
        print 'Running proxy installer with the following options:', dumps(self.options, indent=2, sort_keys=True)

        dist = self.check_os()
        print dist

        # Run packagecloud installation
        #print "Detected %s" % (platform)
        #cmd = "curl -s %s | bash" % (pkg_deb)
        #output = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
