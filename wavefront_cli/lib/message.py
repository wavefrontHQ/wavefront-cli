"""Manage messages for wavefront CLI."""

# pylint: skip-file


class Bcolors:
    """Define different colors for wavefront messages."""

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_welcome():
    """Print wavefront welcome messages."""
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
    """Print header messages."""
    print(Bcolors.HEADER + msg + Bcolors.ENDC)


def print_bold(msg):
    """Print message in Bold."""
    print(Bcolors.BOLD + msg + Bcolors.ENDC)


def print_warn(msg):
    """Print warning messages."""
    print(Bcolors.WARNING + msg + Bcolors.ENDC)


def print_success(msg):
    """Print success message."""
    print(Bcolors.OKBLUE + msg + Bcolors.ENDC)
