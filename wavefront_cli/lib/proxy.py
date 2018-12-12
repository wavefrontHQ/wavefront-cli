import subprocess
import sys

import api
import message
import system

proxy_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
proxy_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"

proxy_next_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy-next/script.deb.sh"
proxy_next_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy-next/script.rpm.sh"



def get_proxy_install_cmd(proxy_next):
    # dist = self.check_os()
    dist = system.check_os()
    if not dist:
        print "Error: Unsupported OS version. Please contact support@wavefront.com."
        return None

    if proxy_next:
        message.print_bold("Using proxy-next option. This will install the latest beta version proxy.")

    print "Detected ", dist
    if dist == "Oracle Linux Server" or dist.strip() == "Fedora" or \
            dist == "Red Hat Enterprise Linux Server" or dist == "Red Hat Enterprise Linux Workstation" or \
            dist == "CentOS" or dist == "CentOS Linux" or dist.startswith("Amazon Linux"):

        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = "curl -s %s | bash" % (pkg)
        cmd += " && yum -y -q install wavefront-proxy"
        return cmd
    elif dist == "Ubuntu" or dist == "debian":

        pkg = proxy_pkg_deb
        if proxy_next:
            pkg = proxy_next_pkg_deb

        cmd = "curl -s %s | bash" % (pkg)
        cmd += " && apt-get -y -q install wavefront-proxy"
        return cmd
    elif dist.strip() == "openSUSE" or dist.strip() == "SUSE Linux Enterprise Server":

        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = "curl -s %s | bash" % (pkg)
        cmd += " && zypper install wavefront-proxy"
        return cmd
    else:
        print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)
        return None


def install_proxy(proxy_next):

    message.print_bold("Starting Wavefront Proxy Installation!")
    cmd = get_proxy_install_cmd(proxy_next)
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
    cmd = "sed -i -e '/token=/c\ttoken=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (token)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # replace server url
    cmd = "sed -i -e '/server=/c\tserver=%s' /etc/wavefront/wavefront-proxy/wavefront.conf" % (url)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # restart proxy
    ret_code = system.restart_service("wavefront-proxy")
    if ret_code > 0:
        message.print_warn("Error restarting proxy service")
        return False

    message.print_success("Finished Wavefront Proxy Configuration!")
    message.print_success("The Proxy's configuration file can be found at /etc/wavefront/wavefront-proxy/wavefront.conf")

    return True
