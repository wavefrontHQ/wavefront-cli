
import system
import api
import subprocess
import message
import sys

proxy_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
proxy_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"

def get_proxy_install_cmd():
    # dist = self.check_os()
    dist = system.check_os()
    print "Detected ", dist
    if dist == "Amazon Linux AMI" or dist == "Red Hat Enterprise Linux Server":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_rpm)
        cmd += " && sudo yum -y -q install wavefront-proxy"
        return cmd
    elif dist == "Ubuntu":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_deb)
        cmd += " && sudo apt-get -y -q install wavefront-proxy"
        return cmd
    else:
        print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)
        return None


def install_proxy():

    message.print_bold("Starting Wavefront Proxy Installation!")
    cmd = get_proxy_install_cmd()
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error installing proxy: " + sys.exc_info()[0])
        return False
    else:
        message.print_success("Finished Wavefront Proxy Installation!")
        return True


def configure_proxy(url, token):
    message.print_bold("Starting Wavefront Proxy Configuration!")
    url = api.clean_url(url) + "/api/"
    print url
    print token

    # replace token
    cmd = "sudo sed -i -e '/token=/c\ttoken=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (token)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error configuring proxy: " + sys.exc_info()[0])
        return False

    # replace server url
    cmd = "sudo sed -i -e '/server=/c\tserver=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (url)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error configuring proxy: " + sys.exc_info()[0])
        return False

    # restart proxy
    ret_code = system.restart_service("wavefront-proxy")
    if ret_code > 0:
        message.print_warn("Error restarting proxy service: " + sys.exc_info()[0])
        return False

    message.print_success("Finished Wavefront Proxy Installation!")

    return True