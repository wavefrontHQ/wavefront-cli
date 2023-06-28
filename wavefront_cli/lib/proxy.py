"""Manage wavefront(Install/configure) proxy."""

from __future__ import print_function

import subprocess

from . import api
from . import message
from . import system


def get_proxy_install_cmd(proxy_next):
    """Get proxy installation command for an operating system."""
    # dist = self.check_os()
    proxy_pkg_deb = ("https://packagecloud.io/install/repositories/"
                     "wavefront/proxy/script.deb.sh")
    proxy_pkg_rpm = ("https://packagecloud.io/install/repositories/"
                     "wavefront/proxy/script.rpm.sh")

    proxy_next_pkg_deb = ("https://packagecloud.io/install/repositories/"
                          "wavefront/proxy-next/script.deb.sh")
    proxy_next_pkg_rpm = ("https://packagecloud.io/install/repositories/"
                          "wavefront/proxy-next/script.rpm.sh")
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

    cmd = "curl -s {pkg} | bash && "
    if dist.strip().startswith(("Oracle Linux Server", "Fedora",
                                "Amazon Linux", "CentOS",
                                "Red Hat Enterprise Linux")):
        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = cmd.format(pkg=pkg) + "yum -y -q install wavefront-proxy"
    elif dist.strip().lower().startswith(("ubuntu", "debian")):
        pkg = proxy_pkg_deb
        if proxy_next:
            pkg = proxy_next_pkg_deb

        cmd = cmd.format(pkg=pkg) + "apt-get -y -q install wavefront-proxy"
    elif dist.strip().startswith(("openSUSE", "SUSE Linux Enterprise Server",
                                  "SLES")):
        pkg = proxy_pkg_rpm
        if proxy_next:
            pkg = proxy_next_pkg_rpm

        cmd = cmd.format(pkg=pkg) + "zypper install wavefront-proxy"
    else:
        print(f"Error: Unsupported OS version: {dist}. Please contact"
              " support@wavefront.com.")
    return cmd


def install_proxy(proxy_next):
    """Install wavefront proxy."""
    message.print_bold("Starting Wavefront Proxy Installation!")
    cmd = get_proxy_install_cmd(proxy_next)
    install_status = False
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        message.print_warn("Unable to install Wavefront Proxy")
    else:
        message.print_success("Finished Wavefront Proxy Installation!")
        install_status = True
    return install_status


# pylint: disable=too-many-arguments
def configure_proxy(url, wavefront_api_token, csp_api_token=None,
                    csp_app_id=None, csp_app_secret=None, csp_org_id=None):
    """Configure wavefront proxy."""
    message.print_bold("Starting Wavefront Proxy Configuration!")
    url = api.clean_url(url) + "/api/"
    print(url)
    if csp_app_id and csp_app_secret and csp_org_id:
        # replace csp oauth app id
        cmd = ('sed', '-i', '-e',
               f'/#cspAppId=/c\tcspAppId={csp_app_id}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSP app ID {csp_app_id}")

        # replace CSP OAuth app secret
        cmd = ('sed', '-i', '-e',
               f'/#cspAppSecret=/c\tcspAppSecret={csp_app_secret}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSP app secret {csp_app_secret}")

        # replace csp org id
        cmd = ('sed', '-i', '-e',
               f'/#cspOrgId=/c\tcspOrgId={csp_org_id}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSO org ID {csp_org_id}")
    if csp_api_token:
        # replace csp api token
        cmd = ('sed', '-i', '-e',
               f'/#cspAPIToken=/c\tcspAPIToken={csp_api_token})',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" csp API token {csp_api_token}")
    if wavefront_api_token:
        # replace token
        cmd = ('sed', '-i', '-e',
               f'/token=/c\ttoken={wavefront_api_token}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" Wavefront API token {wavefront_api_token}")

    # replace server url
    cmd = ('sed', '-i', '-e', f'/server=/c\tserver={url}',
           '/etc/wavefront/wavefront-proxy/wavefront.conf')

    ret_code = system.run_cmd(cmd)
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
