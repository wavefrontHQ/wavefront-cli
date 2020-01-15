"""Manage OS level commands like start/stop service."""

from __future__ import print_function

import subprocess
import sys
import time

import distro

from . import message


def check_os():
    """Check OS distribution."""
    distribution = None
    try:
        distribution = distro.linux_distribution()[0]
    except OSError:
        print("Unable to detect Linux distribution. ", sys.exc_info())

    return distribution


def run_command(cmd):
    """Run OS commands."""
    try:
        ret_code = subprocess.call(cmd, shell=True)
        return ret_code
    except (OSError, ValueError):
        message.print_warn('Error running command: "%s"' % (cmd))
        return 1


def restart_service(service_name):
    """Restart a service."""
    print("Restarting %s" % (service_name))
    time.sleep(3)
    cmd = "service %s restart" % (service_name)
    return run_command(cmd)
    # sys.exc_info()


def write_file(path, text):
    """Write text to file."""
    try:
        file_ref = open(path, "w")
        file_ref.write(text)
        file_ref.close()
        return True
    except IOError:
        message.print_warn("Unable to write file at " + path + ": "
                           + str(sys.exc_info()))
        return False


def remove_service(service_name):
    """Delete a service."""
    dist = check_os()
    print("Detected ", dist)
    if dist.startswith("Amazon Linux") or\
            dist == "Red Hat Enterprise Linux Server":
        cmd = "yum -y remove " + service_name
    elif dist == "Ubuntu":
        cmd = "apt-get -y remove " + service_name
    else:
        print("Error: Unsupported OS version: %s." % (dist))

    print("Running ", cmd)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print("Error removing service %s. Please check the output"
              " above this message." % service_name)

    return ret_code
