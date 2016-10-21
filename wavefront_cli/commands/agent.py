"""The agent command.
wave agent [--proxy-address=<address>] [--proxy-port=<port>]
"""

from json import dumps
import platform
import sys
import subprocess
from .base import Base
import wavefront.system


class Agent(Base):
    """Install the Wavefront Proxy."""

    pkg_deb = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.deb.sh"
    pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.rpm.sh"
    telegraf_conf = "https://gist.githubusercontent.com/ezeev/435d1e7550a1ddf97fb5f3bec1385f21/raw/c1aa176cdbf5e9c8d4d8fb1dc134d12783b98b01/telegraf.conf"

    def get_proxy_info(self):
        proxy_info = {}
        if self.options['--proxy-address']:
            proxy_info['address'] = self.options['--proxy-address']
        else:
            proxy_info['address'] = raw_input("Please enter the address to a running Wavefront proxy on your network? (default = localhost) \n") or "localhost"

        if self.options['--proxy-port']:
            proxy_info['port'] = self.options['--proxy-port']
        else:
            proxy_info['port'] = raw_input("Please enter the address to a running Wavefront proxy on your network? (default = 4242) \n") or "4242"
        return proxy_info

    def uninstall_agent(self):
        cmd = self.get_remove_cmd()
        print "Running ", cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error removing proxy. Please check the output above this message."

    def install_agent(self):
        cmd = self.get_install_cmd()
        print "Running ", cmd
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error installing proxy. Please check the installation output above this message."

    def configure_agent(self, proxy_info):
        # download the template config
        # curl -o /tmp/telegraf.rpm https://dl.influxdata.com/telegraf/releases/telegraf-1.0.0_beta3.x86_64.rpm
        print "Downloading template configuration to /etc/telegraf/telegraf.conf"
        cmd = "sudo curl -o /etc/telegraf/telegraf.conf %s" % (Agent.telegraf_conf)
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error downloading telegraf config file."
            sys.exit(0)
        print "Configuring telegraf config file"
        cmd = 'sudo sed -i -e "s/PROXYHOST/%s/g" /etc/telegraf/telegraf.conf && sudo sed -i -e "s/PROXYPORT/%s/g" /etc/telegraf/telegraf.conf' % (proxy_info['address'],proxy_info['port'])
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error modifying telegraf config file."
            sys.exit(0)

        print "Restarting Telegraf"
        cmd = "sudo service telegraf restart"
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            print "Error restarting Telegraf service."
            sys.exit(0)

    def get_remove_cmd(self):
        dist = wavefront.system.check_os()
        print "Detected ", dist
        if dist == "Amazon Linux AMI":
            cmd = "sudo service telegraf stop"
            cmd += " && sudo yum -y remove telegraf"
            return cmd
        elif dist == "Ubuntu":
            cmd = "sudo service telegraf stop"
            cmd += " && sudo apt-get -y remove telegraf"
            return cmd
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)


    def get_install_cmd(self):
        dist = wavefront.system.check_os()
        print "Detected ", dist
        if dist == "Amazon Linux AMI":
            cmd = "curl -s %s | sudo bash" % (Agent.pkg_rpm)
            cmd += " && sudo yum -y -q install telegraf"
            return cmd
        elif dist == "Ubuntu":
            cmd = "curl -s %s | sudo bash" % (Agent.pkg_deb)
            cmd += " && sudo apt-get -y -q install telegraf"
            return cmd
        else:
            print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)

    def run(self):

        if self.options['install']:
            proxy_info = self.get_proxy_info()
            self.install_agent()
            self.configure_agent(proxy_info)
            print "Agent installation finished"
        elif self.options['remove']:
            self.uninstall_agent()
            print "Agent uninstall finished"




