"""The proxy command."""
from json import dumps
from .base import Base
# wavefront API functions
from wavefront.api import validate_token, clean_url
import wavefront.auth

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
            cmd += " && sudo yum -y -q install wavefront-proxy"
            return cmd
        elif dist == "Ubuntu":
            return Proxy.pkg_deb
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)

    def install_proxy(self):
        cmd = self.get_install_cmd()
        print cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error installing proxy. Please check the installation output above this line."

    def configure_proxy(self,url,token):
        url = clean_url(url) + "/api/"
        print url
        print token
        # replace token
        cmd = "sudo sed -i -e '/token=/c\ttoken=%s' /opt/wavefront/wavefront-proxy/conf/wavefront.conf" % (token)
        subprocess.call(cmd, shell=True)

        # replace server url
        cmd = "sudo sed -i -e '/server=/c\tserver=%s' /opt/wavefront/wavefront-proxy/conf/wavefront.conf" % (url)
        subprocess.call(cmd, shell=True)

        # restart proxy
        ret_code = subprocess.call("sudo service wavefront-proxy restart", shell=True)

    def run(self):

        print 'Running proxy installer with the following options:', dumps(self.options, indent=2, sort_keys=True)
        # wf_url = self.options['--wavefront-url']
        # api_token = self.options['--api-token']
        creds = wavefront.auth.get_or_set_auth(self.options)
        if creds == None:
            print "Unable to obtain Wavefront API credentials."
            sys.exit(0)

        wf_url = creds['user_url']
        api_token = creds['user_token']
        # 1) Validate token
        #valid_token = self.validate_token(wf_url,api_token)
        valid_token = validate_token(wf_url, api_token)
        if not valid_token:
            sys.exit(0)


        # 2) Run packagecloud installation
        print "Running proxy installation"
        self.install_proxy()

        # 3) Configure proxy
        print "Configuring proxy"
        self.configure_proxy(wf_url,api_token)
