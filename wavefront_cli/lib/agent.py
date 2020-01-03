"""Manage Telegraf agent."""


import sys

from . import message
from . import system


CONF_PATH = "/etc/telegraf/telegraf.conf"


def get_install_agent_cmd():
    """Get OS specific command to install Telegraf agent."""
    agent_pkg_deb = "https://packagecloud.io/install/repositories/" \
                    "wavefront/telegraf/script.deb.sh"
    agent_pkg_rpm = "https://packagecloud.io/install/repositories/" \
                    "wavefront/telegraf/script.rpm.sh"
    dist = system.check_os()
    cmd = None
    if not dist:
        print("Error: Unsupported OS version. Please contact"
              " support@wavefront.com.")
        return cmd

    # pylint: disable=R0916
    if dist == "Oracle Linux Server" or dist.strip() == "Fedora" or \
            dist == "Red Hat Enterprise Linux Server" or\
            dist == "Red Hat Enterprise Linux Workstation" or \
            dist == "CentOS" or dist == "CentOS Linux" or\
            dist.startswith("Amazon Linux"):
        cmd = "curl -s %s | bash" % (agent_pkg_rpm)
        cmd += " && yum -y -q install telegraf"
    elif dist == "Ubuntu":
        cmd = "curl -s %s | bash" % (agent_pkg_deb)
        cmd += ' && apt-get -y -qq -o Dpkg::Options::="--force-confold"' \
               ' install telegraf'
    elif dist == "debian":
        cmd = "curl -s %s | bash" % (agent_pkg_deb)
        cmd += ' && apt-get -o Dpkg::Options::="--force-confnew"' \
               ' -y install telegraf'
    elif dist.strip() == "openSUSE" or\
            dist.strip() == "SUSE Linux Enterprise Server" or \
            dist.strip() == "SLES":
        cmd = "curl -s %s | bash" % (agent_pkg_rpm)
        cmd += ' && zypper install telegraf'
    else:
        message.print_warn("Error: Unsupported OS version: %s." % (dist))

    return cmd


def tag_telegraf_config(comment, tags):
    """Add custom tags into Telegraf."""
    message.print_bold("Adding custom tags to Telegraf configuration")

    tags_pre = "- %s -" % (comment)
    tags_post = "- end %s tags - " % (comment)
    tag_str = "  # %s\n" % (tags_pre)
    for key, value in list(tags.items()):
        tag_str += '  %s = "%s"\n' % (key.lower(), value)
    tag_str += "  # %s\n" % (tags_post)
    try:
        tag_txt = open("tags.txt", "w")
        tag_txt.write(tag_str)
        tag_txt.close()
    except IOError:
        message.print_warn("Error writing tags.txt: " + sys.exc_info())
        return False

    # remove existing ec2 tags
    conf = CONF_PATH
    # pylint: disable=W1401
    cmd = "sed -i '/%s/,/%s/d' %s" % (tags_pre, tags_post, conf)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error adding tags to Telegraf configuration")
        return False

    cmd = "sed -i '/\[global_tags\]/r tags.txt' %s" % (conf)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error overwriting telegraf.conf."
                           " Is the file located at " + conf + "? ")

    message.print_success("Finished adding tags to Telegraf configuration.")
    return True


def install_agent():
    """Install Telegraf."""
    telegraf_conf = "https://raw.githubusercontent.com/wavefrontHQ/" \
                    "integrations/master/telegraf/telegraf.conf"
    message.print_bold("Starting Telegraf Installation!")
    print("Downloading configuration to ", CONF_PATH)

    cmd = "mkdir -p /etc/telegraf && sudo curl -o %s %s"\
          % (CONF_PATH, telegraf_conf)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error downloading Telegraf config file.")
        return False

    cmd = get_install_agent_cmd()
    print("Running ", cmd)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error installing Telegraf")
        return False

    message.print_success("Finished Installing Telegraf!")
    message.print_success("The Telegraf configuration file can be found"
                          " at /etc/telegraf/telegraf.conf")
    return True
