"""The proxy command."""
from json import dumps
from .base import Base
# wavefront API functions
from wavefront.api import validate_token, clean_url
import wavefront.auth
import wavefront.system

import subprocess
import json
import os
import sys
import platform

class Proxy(Base):
    """Install the Wavefront Proxy."""

    pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
    pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"

    '''
    def check_os(self):
        try:
            if platform.linux_distribution() == ('', '', ''):
                #aws linux workaround
                if platform.linux_distribution(supported_dists=['system'])[0] != None:
                    return platform.linux_distribution(supported_dists=['system'])[0]
            else:
                return platform.linux_distribution[0]
        except:
            print "Unable to detect Linux distribution. ", sys.exc_info()
    '''

    def get_remove_cmd(self):
        # dist = self.check_os()
        dist = wavefront.system.check_os()
        print "Detected ", dist
        if dist == "Amazon Linux AMI":
            cmd = "sudo yum -y remove wavefront-proxy"
            return cmd
        elif dist == "Ubuntu":
            cmd = "sudo apt-get -y remove wavefront-proxy"
            return cmd
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)

    def get_install_cmd(self):
        # dist = self.check_os()
        dist = wavefront.system.check_os()
        print "Detected ", dist
        if dist == "Amazon Linux AMI":
            cmd = "curl -s %s | sudo bash" % (Proxy.pkg_rpm)
            cmd += " && sudo yum -y -q install wavefront-proxy"
            return cmd
        elif dist == "Ubuntu":
            cmd = "curl -s %s | sudo bash" % (Proxy.pkg_deb)
            cmd += " && sudo apt-get -y -q install wavefront-proxy"
            return cmd
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)


    def uninstall_proxy(self):
        cmd = self.get_remove_cmd()
        print "Running ", cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error removing proxy. Please check the output above this message."

    def install_proxy(self):
        cmd = self.get_install_cmd()
        print "Running ", cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error installing proxy. Please check the installation output above this message."

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

        print 'Running proxy installer'

        if self.options['remove']:
            self.uninstall_proxy()
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
            self.install_proxy()

            # 2) Configure proxy
            print "Configuring proxy"
            self.configure_proxy(wf_url,api_token)
        else:
            print 'You must pass either the "install" or "remove" flag to the proxy command. Run "wave -h" for more information.'
