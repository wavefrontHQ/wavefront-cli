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

    cmd = "curl -s {} | bash && "
    if dist.strip().startswith(("Oracle Linux Server", "Fedora",
                                "Amazon Linux", "CentOS",
                                "Red Hat Enterprise Linux")):
        cmd = cmd.format(agent_pkg_rpm) + "yum -y -q install telegraf"
    elif dist.strip().startswith("Ubuntu"):
        cmd = (cmd.format(agent_pkg_deb) + "apt-get -y -qq -o D"
               'pkg::Options::="--force-confold" install telegraf')
    elif dist.strip().lower().startswith("debian"):
        cmd = (cmd.format(agent_pkg_deb) + "apt-get -o D"
               'pkg::Options::="--force-confnew" -y install telegraf')
    elif dist.strip().startswith(("openSUSE", "SUSE Linux Enterprise Server",
                                  "SLES")):
        cmd = cmd.format(agent_pkg_rpm) + "zypper install telegraf"
    else:
        message.print_warn(f"Error: Unsupported OS version: {dist}.")

    return cmd


def tag_telegraf_config(comment, tags):
    """Add custom tags into Telegraf."""
    message.print_bold("Adding custom tags to Telegraf configuration")

    tags_pre = f"- {comment} -"
    tags_post = f"- end {comment} tags - "
    tag_strings = [f"  # {tags_pre}"]
    for key, value in tags.items():
        tag_strings.append(f'  {key.lower()} = "{value}"')
    tag_strings.append(f"  # {tags_post}")
    try:
        with open("tags.txt", "w", encoding="utf-8") as tag_txt:
            tag_txt.writelines(tag_strings)
    except IOError:
        message.print_warn("Error writing tags.txt: " + sys.exc_info())
        return False

    # remove existing ec2 tags
    conf = CONF_PATH
    cmd = f"sed -i '/{tags_pre}/,/{tags_post}/d' {conf}"

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error adding tags to Telegraf configuration")
        return False

    cmd = rf"sed -i '/\[global_tags\]/r tags.txt' {conf}"

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

    cmd = f"mkdir -p /etc/telegraf && sudo curl -o {CONF_PATH} {telegraf_conf}"

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
