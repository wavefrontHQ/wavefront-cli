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

    def get_install_cmd(self):
        dist = self.check_os()
        print "Detected ", dist
        if dist == "Amazon Linux AMI":
            cmd = "curl -s %s | sudo bash" % (Proxy.pkg_rpm)
            cmd += "&& sudo yum -y -q install wavefront-proxy"
            return cmd
        elif dist == "Ubuntu":
            return Proxy.pkg_deb
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)

    def run(self):
        print 'Hello from proxy'
        print 'Running proxy installer with the following options:', dumps(self.options, indent=2, sort_keys=True)

        # Run packagecloud installation
        print "Running proxy installation"
        cmd = self.get_install_cmd()
        print cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error installing proxy. Please check the installation logs above this line."
