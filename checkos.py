import platform

def check_os():
    try:
        if platform.linux_distribution() == ('', '', ''):
            # aws linux workaround
            if platform.linux_distribution(supported_dists=['system'])[0] != None:
                print platform.linux_distribution(supported_dists=['system'])[0]
        else:
            print platform.linux_distribution()[0]
    except:
        print "Unable to detect Linux distribution. ", sys.exc_info()


check_os()