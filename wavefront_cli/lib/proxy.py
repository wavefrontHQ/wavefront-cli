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
               f'/cspAppId=/c\tcspAppId={csp_app_id}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSP app ID {csp_app_id}")

        # replace CSP OAuth app secret
        cmd = ('sed', '-i', '-e',
               f'/cspAppSecret=/c\tcspAppSecret={csp_app_secret}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSP app secret {csp_app_secret}")

        # replace csp org id
        cmd = ('sed', '-i', '-e',
               f'/cspOrgId=/c\tcspOrgId={csp_org_id}',
               '/etc/wavefront/wavefront-proxy/wavefront.conf')
        ret_code = system.run_cmd(cmd)
        if ret_code > 0:
            message.print_warn("Error Configuring Wavefront Proxy with"
                               f" CSO org ID {csp_org_id}")
    if csp_api_token:
        # replace csp api token
        cmd = ('sed', '-i', '-e',
               f'/cspAPIToken=/c\tcspAPIToken={csp_api_token}',
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


def configure_csp_oauth_options():
    """Configure the CSP OAuth app options.

    Returns:
        None
    """
    lines_to_append = [
        "\n# To add a proxy, you need to use an existing App ID, "
        "App Secret for server to serve type of app with AOA "
        "service proxy role.",
        "# If you have no App ID and App Secret yet, "
        "you can create one for server to serve type "
        "of app under Organization/OAuth",
        "# Apps menu item in VMWare Cloud Service."
        " Note: Proxy, based on OAuth apps, "
        "has no expiration time.",
        "#cspAppId=CSP_APP_SECRET_HERE"
    ]
    add_option("cspAppId=", lines_to_append)

    lines_to_append = [
        "\n# To add a proxy, you need to use an existing App ID, "
        "App Secret for server to serve type of app with AOA "
        "service proxy role.",
        "# If you have no App ID and App Secret yet, "
        "you can create one for server to serve type of app under "
        "Organization/OAuth",
        "# Apps menu item in VMWare Cloud Service. "
        "Note: Proxy, based on OAuth apps, "
        "has no expiration time.",
        "#cspAppSecret=CSP_APP_SECRET_HERE"
    ]
    add_option("cspAppSecret=", lines_to_append)

    lines_to_append = [
        "\n# The CSP organisation ID.",
        "#cspOrgId=CSP_ORG_ID_HERE"
    ]
    add_option("cspOrgId=", lines_to_append)

    lines_to_append = [
        "\n# CSP console URL. This will be "
        "used in many places like getting token.",
        "#cspBaseUrl=https://console.cloud.vmware.com"
    ]
    add_option("cspBaseUrl=", lines_to_append)


def configure_csp_api_token_options():
    """Configure the CSP API token options.

    Returns:
        None
    """
    lines_to_append = [
        "\n# To add a proxy, you need to use an "
        "existing API token with AOA service proxy role. "
        "If you have no API token yet, you",
        "# can create one under your account "
        "page in VMWare Cloud Service.",
        "#cspAPIToken=CSP_API_TOKEN_HERE"
    ]
    add_option("cspAPIToken=", lines_to_append)

    lines_to_append = [
        "\n# CSP console URL. This will be used "
        "in many places like getting token.",
        "#cspBaseUrl=https://console.cloud.vmware.com"
    ]
    add_option("cspBaseUrl=", lines_to_append)


def configure_wavefront_api_token_options():
    """Configure the Wavefront API token options.

    Returns:
        None
    """
    lines_to_append = [
        "\n# The Token is any valid API token for "
        "an account that has *Proxy Management* permissions. "
        "To get to the token:",
        "# 1. Click the gear icon at the top right "
        "in the Wavefront UI.",
        "# 2. Click your account name (usually your email)",
        "# 3. Click *API access*.",
        "#token=WF_TOKEN_HERE"
    ]
    add_option("token=", lines_to_append)


def comment_auth_methods(csp_api_token, csp_oauth_app, wavefront_api_token):
    """Comment out specific authentication-related methods.

    Args:
    csp_api_token (bool): Flag indicating whether
    to comment out cspAPIToken line.
    csp_oauth_app (bool): Flag indicating whether to
    comment out cspAppId, cspAppSecret, cspOrgId,
    and cspBaseUrl lines.
    wavefront_api_token (bool): Flag indicating
    whether to comment out token=WF_TOKEN_HERE line.

    Returns:
        None
    """
    config_file = '/etc/wavefront/wavefront-proxy/wavefront.conf'

    options_to_comment = []

    if wavefront_api_token:
        options_to_comment.append('token=')

    if csp_oauth_app:
        options_to_comment.extend(['cspAppId=',
                                   'cspAppSecret=',
                                   'cspOrgId=',
                                   'cspBaseUrl='])

    if csp_api_token:
        options_to_comment.extend(['cspAPIToken=', 'cspBaseUrl='])

    with open(config_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if any(line.strip().startswith(option) for option
               in options_to_comment) and not line.startswith('#'):
            lines[i] = '#' + line.lstrip()

    with open(config_file, 'w', encoding="utf-8") as file:
        file.writelines(lines)


def add_option(option, lines_to_append):
    """Add the missing option.

    Add the missing option(wf token,
    csp api token or csp oauth app) option
    to a configuration file if the option does not already exist.

    Args:
    option (str): The option to check for in the configuration file.
    lines_to_append (list): A list of lines to append to
    the configuration file.

    Returns:
        None
    """
    config_file = '/etc/wavefront/wavefront-proxy/wavefront.conf'
    option_found = False

    with open(config_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(option) or line.startswith("#" + option):
                option_found = True
                break

    if not option_found:
        with open(config_file, 'a', encoding="utf-8") as file:
            file.write('\n')
            for line in lines_to_append:
                file.write(line + '\n')
