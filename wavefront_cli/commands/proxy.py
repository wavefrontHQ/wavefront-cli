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
        url = self.clean_url(url)

        # /daemon/test?token=$TOKEN
        validate_url = "%s/api/daemon/test?token=%s" % (url,token)
        print validate_url
        r = requests.post(validate_url)
        status_code = r.status_code
        if status_code == 401:
            print "Error validating token: Unauthorized. Make sure your Wavefront account has Agent Management permissions."
            return False
        elif status_code == 200:
            print "Successfully validated token."
            return True
        elif status_code == 400:
            print "Url not found. Please check that your Wavefront URL is valid and that this machine has http access."
            return False


    def clean_url(self,url):
        url = url
        if url.endswith("/api/"):
            url = url[:-5]
        elif url.endswith("/api"):
            url = url[:-4]
        elif url.endswith("/"):
            url = url[:-1]
        return url


    def configure_proxy(self,url,token):
        url = self.clean_url(url) + "/api/"
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
        wf_url = self.options['--wavefront-url']
        api_token = self.options['--api-token']

        # 1) Validate token
        valid_token = self.validate_token(wf_url,api_token)
        if not valid_token:
            sys.exit(0)

        # 2) Run packagecloud installation
        print "Running proxy installation"
        self.install_proxy()

        # 3) Configure proxy
        print "Configuring proxy"
        self.configure_proxy(wf_url,api_token)
