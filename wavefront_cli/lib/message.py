class Bcolors:
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
    print(Bcolors.HEADER + msg + Bcolors.ENDC)


def print_bold(msg):
    print(Bcolors.BOLD + msg + Bcolors.ENDC)


def print_warn(msg):
    print(Bcolors.WARNING + msg + Bcolors.ENDC)


def print_success(msg):
    print(Bcolors.OKBLUE + msg + Bcolors.ENDC)
