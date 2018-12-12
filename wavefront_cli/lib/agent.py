import subprocess
import sys

import message
import system
import aws

agent_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.deb.sh"
agent_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.rpm.sh"
telegraf_conf = "https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf"
conf_path = "/etc/telegraf/telegraf.conf"


def get_install_agent_cmd():
    dist = system.check_os()
    if not dist:
        print "Error: Unsupported OS version. Please contact support@wavefront.com."
        return None
    if dist == "Oracle Linux Server" or dist.strip() == "Fedora" or \
            dist == "Red Hat Enterprise Linux Server" or dist == "Red Hat Enterprise Linux Workstation" or \
            dist == "CentOS" or dist == "CentOS Linux" or dist.startswith("Amazon Linux"):
        cmd = "curl -s %s | bash" % (agent_pkg_rpm)
        cmd += " && yum -y -q install telegraf"
        return cmd
    elif dist == "Ubuntu":
        cmd = "curl -s %s | bash" % (agent_pkg_deb)
        cmd += ' && apt-get -y -qq -o Dpkg::Options::="--force-confold" install telegraf'
        return cmd
    elif dist == "debian":
        cmd = "curl -s %s | bash" % (agent_pkg_deb)
        cmd += ' && apt-get -o Dpkg::Options::="--force-confnew" -y install telegraf'
        return cmd
    elif dist.strip() == "openSUSE" or dist.strip() == "SUSE Linux Enterprise Server":
        cmd = "curl -s %s | bash" % (agent_pkg_rpm)
        cmd += ' && zypper install telegraf'
        return cmd
    else:
        message.print_warn("Error: Unsupported OS version: %s." % (dist))
        return None

def tag_telegraf_config(comment, tags):

    message.print_bold("Adding custom tags to Telegraf configuration")

    tags_pre = "- %s -" % (comment)
    tags_post = "- end %s tags - " % (comment)
    tagStr = "  # %s\n" % (tags_pre)
    for k,v in tags.iteritems():
        tagStr += '  %s = "%s"\n' % (k.lower(),v)
    tagStr += "  # %s\n" % (tags_post)
    try:
        tagTxt = open("tags.txt","w")
        tagTxt.write(tagStr)
        tagTxt.close()
    except:
        message.print_warn("Error writing tags.txt: " + sys.exc_info())
        return False

    # remove existing ec2 tags
    conf = conf_path
    cmd = "sed -i '/%s/,/%s/d' %s" % (tags_pre, tags_post, conf)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error adding tags to Telegraf configuration")
        return False

    cmd = "sed -i '/\[global_tags\]/r tags.txt' %s" % (conf)

    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error overwriting telegraf.conf. Is the file located at " + conf + "? ")


    message.print_success("Finished adding tags to Telegraf configuration.")
    return True


def install_agent():

    message.print_bold("Starting Telegraf Installation!")
    print "Downloading configuration to ", conf_path

    cmd = "mkdir -p /etc/telegraf && sudo curl -o %s %s" % (conf_path,telegraf_conf)
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error downloading Telegraf config file.")
        return False

    cmd = get_install_agent_cmd()
    print "Running ", cmd
    ret_code = system.run_command(cmd)
    if ret_code > 0:
        message.print_warn("Error installing Telegraf")
        return False

    message.print_success("Finished Installing Telegraf!")
    message.print_success("The Telegraf configuration file can be found at /etc/telegraf/telegraf.conf")
    return True
