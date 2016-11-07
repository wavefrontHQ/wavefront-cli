
import platform
import subprocess

def check_os():
    try:
        if platform.linux_distribution() == ('', '', ''):
            # aws linux workaround
            if platform.linux_distribution(supported_dists=['system'])[0] != None:
                return platform.linux_distribution(supported_dists=['system'])[0]
        else:
            return platform.linux_distribution[0]
    except:
        print "Unable to detect Linux distribution. ", sys.exc_info()


def restart_service(service_name):
    print "Restarting %s" % (service_name)
    cmd = "sudo service %s restart" % (service_name)
    ret_code = subprocess.call(cmd, shell=True)
    return ret_code


def remove_service(service_name):
    dist = check_os()
    print "Detected ", dist
    if dist == "Amazon Linux AMI":
        cmd = "sudo yum -y remove " + service_name
    elif dist == "Ubuntu":
        cmd = "sudo apt-get -y remove " + service_name
    else:
        print "Error: Unsupported OS version: %s. Please contact support@wavefront.com." % (dist)

    print "Running ", cmd
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print "Error removing service %s. Please check the output above this message." % (service_name)

    return ret_code


