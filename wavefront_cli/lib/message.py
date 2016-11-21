class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_welcome():
    msg = """
         __      __                     _____                      __
        /  \    /  \_____ ___  __ _____/ ____\______  ____   _____/  |_
        \   \/\/   /\__   \  \/ // __ \   __\ _  __ \/  _ \ /    \   __
         \        /  / __  \   /\  ___/|  |   |  | \(  <_> )   |  \  |
          \__/\  /  (____  /\_/  \___  >__|   |__|   \____/|___|  /__|
               \/        \/          \/                         \/

                """
    print_success(msg)

def print_header(msg):
    print bcolors.HEADER + msg + bcolors.ENDC

def print_bold(msg):
    print bcolors.BOLD + msg + bcolors.ENDC

def print_warn(msg):
    print bcolors.WARNING + msg + bcolors.ENDC

def print_success(msg):
    print bcolors.OKBLUE + msg + bcolors.ENDC