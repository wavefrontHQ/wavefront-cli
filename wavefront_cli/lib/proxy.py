import subprocess
import sys

import api
import message
import system

proxy_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
proxy_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"

def get_proxy_install_cmd():
    # dist = self.check_os()
    dist = system.check_os()
    print "Detected ", dist
    if dist == "Amazon Linux AMI" or dist == "Red Hat Enterprise Linux Server" or dist == "CentOS" or dist == "CentOS Linux":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_rpm)
        cmd += " && sudo yum -y -q install wavefront-proxy"
        return cmd
    elif dist == "Ubuntu" or dist == "debian":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_deb)
        cmd += " && sudo apt-get -y -q install wavefront-proxy"
        return cmd
    else:
        print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)
        return None


def install_proxy():

    message.print_bold("Starting Wavefront Proxy Installation!")
    cmd = get_proxy_install_cmd()
    try:
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            message.print_warn("Error installing proxy.")
            return False
        else:
            message.print_success("Finished Wavefront Proxy Installation!")
            return True
    except:
        message.print_warn("Unable to install Wavefront Proxy")
        return False


def configure_proxy(url, token):
    message.print_bold("Starting Wavefront Proxy Configuration!")
    url = api.clean_url(url) + "/api/"
    print url
    print token

    # replace token
    cmd = "sudo sed -i -e '/token=/c\ttoken=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (token)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # replace server url
    cmd = "sudo sed -i -e '/server=/c\tserver=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (url)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # restart proxy
    ret_code = system.restart_service("wavefront-proxy")
    if ret_code > 0:
        message.print_warn("Error restarting proxy service: " + sys.exc_info())
        return False

    message.print_success("Finished Wavefront Proxy Installation!")

    return True