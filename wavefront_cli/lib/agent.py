import subprocess
import sys

import message
import system

agent_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.deb.sh"
agent_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.rpm.sh"
telegraf_conf = "https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf"
conf_path = "/etc/telegraf/telegraf.conf"


def get_install_agent_cmd():
    dist = system.check_os()
    if dist == "Amazon Linux AMI" or dist == "Red Hat Enterprise Linux Server":
        cmd = "curl -s %s | sudo bash" % (agent_pkg_rpm)
        cmd += " && sudo yum -y -q install telegraf"
        return cmd
    elif dist == "Ubuntu":
        cmd = "curl -s %s | sudo bash" % (agent_pkg_deb)
        cmd += " && sudo apt-get -y -q install telegraf"
        return cmd
    else:
        message.print_warn("Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist))
        return None

def install_agent():

    message.print_bold("Starting Telegraf Installation!")
    print "Downloading configuration to ", conf_path

    cmd = "sudo mkdir -p /etc/telegraf && sudo curl -o %s %s" % (conf_path,telegraf_conf)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error downloading Telegraf config file.")
        return False

    '''
    print "Modifying Telegraf Wavefront output plugin settings"
    cmd = "sudo sed -i -e \"s/PROXYHOST/%s/g\" /etc/telegraf/telegraf.conf && sudo sed -i -e \"s/PROXYPORT/%s/g\" /etc/telegraf/telegraf.conf" % (proxy_address, proxy_port)
    ret_code = subprocess.call(cmd,shell=True)
    if ret_code > 0:
        message.print_warn("Error updating Telegraf config")
        return False
    '''

    cmd = get_install_agent_cmd()
    print "Running ", cmd
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error installing Telegraf: " + sys.exc_info())
        return False

    message.print_success("Finished Installing Telegraf!")
    return True



