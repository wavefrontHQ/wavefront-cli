"""Script to verify os distribution."""

import platform
import sys


def check_os():
    """Check OS distribution."""
    try:
        if platform.linux_distribution() == ('', '', ''):
            # aws linux workaround
            if platform.linux_distribution(
                    supported_dists=['system'])[0] is not None:
                print(platform.linux_distribution(
                    supported_dists=['system'])[0])
        else:
            print(platform.linux_distribution()[0])
    except Exception:
        print("Unable to detect Linux distribution. " + sys.exc_info())


check_os()
