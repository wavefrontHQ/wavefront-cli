
import system
import subprocess
import sys
import message

agent_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.deb.sh"
agent_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/telegraf/script.rpm.sh"
telegraf_conf = "https://gist.githubusercontent.com/ezeev/435d1e7550a1ddf97fb5f3bec1385f21/raw/d75315af0b122cb6423b358be6919decf6019377/telegraf.conf"
conf_path = "/etc/telegraf/telegraf.conf"

def input_proxy_info(options):
    proxy_info = {}
    if options['--proxy-address']:
        proxy_info['address'] = options['--proxy-address']
    else:
        proxy_info['address'] = raw_input \
            ("Please enter the address to a running Wavefront proxy on your network? (default = localhost) \n") or "localhost"

    if options['--proxy-port']:
        proxy_info['port'] = options['--proxy-port']
    else:
        proxy_info['port'] = raw_input \
            ("Please enter the address to a running Wavefront proxy on your network? (default = 2878) \n") or "2878"
    return proxy_info


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

    cmd = get_install_agent_cmd()
    print "Running ", cmd
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error installing Telegraf: " + sys.exc_info()[0])
        return False
    else:
        message.print_success("Finished Telegraf Installation!")
        return True


#def configure_agent(proxy_info):
def configure_agent(proxy_address,port):

    message.print_bold("Starting Telegraf Configuration!")

    print "Downloading template configuration to ", conf_path
    cmd = "sudo curl -o %s %s" % (conf_path,telegraf_conf)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error downloading telegraf config file.")
        sys.exit(0)
    print "Configuring telegraf config file"
    cmd = 'sudo sed -i -e "s/PROXYHOST/%s/g" /etc/telegraf/telegraf.conf && sudo sed -i -e "s/PROXYPORT/%s/g" /etc/telegraf/telegraf.conf' % (proxy_address, port)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        message.print_warn("Error modifying telegraf config file: " + sys.exc_info()[0])
        return False

    ret_code = system.restart_service('telegraf')
    if ret_code > 0:
        message.print_warn("Error restarting Telegraf service.")
        return False

    message.print_success("Finished Telegraf Configuration!")
    return True
