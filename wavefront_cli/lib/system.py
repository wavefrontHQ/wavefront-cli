import platform
import subprocess
import sys
import time

import message


def check_os():
    try:
        if platform.linux_distribution() == ('', '', ''):
            # aws linux workaround
            if platform.linux_distribution(supported_dists=['system'])[0] != None:
                return platform.linux_distribution(supported_dists=['system'])[0]
        else:
            return platform.linux_distribution()[0]
    except:
        print "Unable to detect Linux distribution. ", sys.exc_info()


def run_command(cmd):
    try:
        ret_code = subprocess.call(cmd, shell=True)
        return ret_code
    except:
        message.print_warn('Error running command: "%s"' % (cmd))
        return 1


def restart_service(service_name):
    print "Restarting %s" % (service_name)
    time.sleep(3)
    cmd = "service %s restart" % (service_name)
    return run_command(cmd)
    # sys.exc_info()



def write_file(path, text):
    try:
        file = open(path,"w")
        file.write(text)
        file.close()
        return True
    except:
        message.print_warn("Unable to write file at " + path + ": " + str(sys.exc_info()))
        return False

def remove_service(service_name):
    dist = check_os()
    print "Detected ", dist
    if dist.startswith("Amazon Linux") or dist == "Red Hat Enterprise Linux Server":
        cmd = "yum -y remove " + service_name
    elif dist == "Ubuntu":
        cmd = "apt-get -y remove " + service_name
    else:
        print "Error: Unsupported OS version: %s." % (dist)

    print "Running ", cmd
    ret_code = subprocess.call(cmd, shell=True)
    if ret_code > 0:
        print "Error removing service %s. Please check the output above this message." % (service_name)

    return ret_code
