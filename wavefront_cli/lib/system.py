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


def run_cmd(cmd):
    """Run OS commands."""
    try:
        subprocess.check_call(cmd)
        return 0
    except subprocess.CalledProcessError:
        message.print_warn(f'Error running command: "{cmd}"')
        return 1


def run_command(cmd):
    """Run OS commands."""
    try:
        ret_code = subprocess.call(cmd, shell=True)
        return ret_code
    except (OSError, ValueError):
        message.print_warn(f'Error running command: "{cmd}"')
        return 1


def restart_service(service_name):
    """Restart a service."""
    print(f"Restarting {service_name}")
    time.sleep(3)
    cmd = f"service {service_name} restart"
    return run_command(cmd)
    # sys.exc_info()


def write_file(path, text):
    """Write text to file."""
    try:
        with open(path, "w", encoding="utf-8") as file_ref:
            file_ref.write(text)
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
        print(f"Error: Unsupported OS version: {dist}.")

    print("Running ", cmd)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print(f"Error removing service {service_name}. "
              "Please check the output above this message.")

    return ret_code
