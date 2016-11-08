
import system
import api
import subprocess

proxy_pkg_deb = "https://packagecloud.io/install/repositories/wavefront/proxy/script.deb.sh"
proxy_pkg_rpm = "https://packagecloud.io/install/repositories/wavefront/proxy/script.rpm.sh"

def get_proxy_install_cmd():
    # dist = self.check_os()
    dist = system.check_os()
    print "Detected ", dist
    if dist == "Amazon Linux AMI":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_rpm)
        cmd += " && sudo yum -y -q install wavefront-proxy"
        return cmd
    elif dist == "Ubuntu":
        cmd = "sudo curl -s %s | sudo bash" % (proxy_pkg_deb)
        cmd += " && sudo apt-get -y -q install wavefront-proxy"
        return cmd
    else:
        print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)
        return None


def install_proxy():
    cmd = get_proxy_install_cmd()
    print "Running ", cmd
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print "Error installing proxy. Please check the installation output above this message."
        return False
    else:
        return True


def configure_proxy(url, token):
    url = api.clean_url(url) + "/api/"
    print url
    print token

    # replace token
    cmd = "sudo sed -i -e '/token=/c\ttoken=%s' /opt/wavefront/wavefront-proxy/conf/wavefront.conf" % (token)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print "Error configuring proxy. Please check the installation output above this message."
        return False

    # replace server url
    cmd = "sudo sed -i -e '/server=/c\tserver=%s' /opt/wavefront/wavefront-proxy/conf/wavefront.conf" % (url)
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print "Error configuring proxy. Please check the installation output above this message."
        return False

    # restart proxy
    ret_code = system.restart_service("wavefront-proxy")
    if ret_code > 0:
        print "Error restarting proxy service. Please check the installation output above this message."
        return False

    return True