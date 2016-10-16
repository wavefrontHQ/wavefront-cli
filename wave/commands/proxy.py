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

    def validate_token(self,url,token):
        # /daemon/test?token=$TOKEN
        

    def configure_proxy(self,url,token):
        print url
        print token
        # replace token
        token_str = "\#token\=XXX"

        cmd = 'sudo sed -i -e "s/%s/token=%s/g" /opt/wavefront/wavefront-proxy/conf/wavefront.conf' % (token_str,token)
        subprocess.call(cmd, shell=True)

        # replace server url
        url_str = "https://try.wavefront.com/api/"
        cmd = "sudo sed -i -e 's,%s,%s,g' /opt/wavefront/wavefront-proxy/conf/wavefront.conf" % (url_str,url)
        subprocess.call(cmd, shell=True)

        # restart proxy
        ret_code = subprocess.call("sudo service wavefront-proxy restart", shell=True)


    def run(self):

        print 'Running proxy installer with the following options:', dumps(self.options, indent=2, sort_keys=True)
        wf_url = self.options['--wavefront-url']
        api_token = self.options['--api-token']
        # Run packagecloud installation
        print "Running proxy installation"
        self.install_proxy()
        print "Configuring proxy"
        self.configure_proxy(wf_url,api_token)
