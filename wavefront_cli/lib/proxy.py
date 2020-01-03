"""Manage wavefront(Install/configure) proxy."""

# pylint: disable=R0801


from __future__ import print_function

import subprocess

from . import api
from . import message
from . import system


def get_proxy_install_cmd(proxy_next):
    """Get proxy installation command for an operating system."""
    # dist = self.check_os()
    proxy_pkg_deb = "https://packagecloud.io/install/repositories/wavefront" \
                    "/proxy/script.deb.sh"
    proxy_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/" \
                    "proxy/script.rpm.sh"

    proxy_next_pkg_deb = "https://packagecloud.io/install/repositories/" \
                         "wavefront/proxy-next/script.deb.sh"
    proxy_next_pkg_rpm = "https://packagecloud.io/install/repositories/" \
                         "wavefront/proxy-next/script.rpm.sh"
    cmd = None
    dist = system.check_os()
    if not dist:
        print("Error: Unsupported OS version. Please contact"
              " support@wavefront.com.")
        return cmd

    if proxy_next:
        message.print_bold("Using proxy-next option. This will"
                           " install the latest beta version proxy.")

    print("Detected ", dist)
    # pylint: disable=R0916
    if dist == "Oracle Linux Server" or dist.strip() == "Fedora" or \
            dist == "Red Hat Enterprise Linux Server" or \
            dist == "Red Hat Enterprise Linux Workstation" or \
            dist == "CentOS" or dist == "CentOS Linux" or\
            dist.startswith("Amazon Linux"):

        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = "curl -s %s | bash" % (pkg)
        cmd += " && yum -y -q install wavefront-proxy"
    elif dist in ("Ubuntu", "debian"):

        pkg = proxy_pkg_deb
        if proxy_next:
            pkg = proxy_next_pkg_deb

        cmd = "curl -s %s | bash" % pkg
        cmd += " && apt-get -y -q install wavefront-proxy"
    elif dist.strip() == "openSUSE" or\
            dist.strip() == "SUSE Linux Enterprise Server" or \
            dist.strip() == "SLES":

        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = "curl -s %s | bash" % pkg
        cmd += " && zypper install wavefront-proxy"
    else:
        print("Error: Unsupported OS version: %s. Please contact"
              " support@wavefront.com." % dist)
    return cmd


def install_proxy(proxy_next):
    """Install wavefront proxy."""
    message.print_bold("Starting Wavefront Proxy Installation!")
    cmd = get_proxy_install_cmd(proxy_next)
    install_status = False
    try:
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            message.print_warn("Error installing proxy.")
        else:
            message.print_success("Finished Wavefront Proxy Installation!")
            install_status = True
    # pylint: disable=W0703
    except Exception:
        message.print_warn("Unable to install Wavefront Proxy")

    return install_status


def configure_proxy(url, token):
    """Configure wavefront proxy."""
    message.print_bold("Starting Wavefront Proxy Configuration!")
    url = api.clean_url(url) + "/api/"
    print(url)
    print(token)

    # replace token
    cmd = "sed -i -e '/token=/c\ttoken=%s' /etc/wavefront/wavefront-proxy/" \
          "wavefront.conf" % (token)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # replace server url
    cmd = "sed -i -e '/server=/c\tserver=%s' /etc/wavefront/wavefront-proxy/" \
          "wavefront.conf" % (url)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error Configuring Wavefront Proxy")

    # restart proxy
    ret_code = system.restart_service("wavefront-proxy")
    if ret_code > 0:
        message.print_warn("Error restarting proxy service")
        return False

    message.print_success("Finished Wavefront Proxy Configuration!")
    message.print_success("The Proxy's configuration file can be found at"
                          " /etc/wavefront/wavefront-proxy/wavefront.conf")

    return True
