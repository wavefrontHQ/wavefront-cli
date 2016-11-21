"""The hello command."""

from .base import Base

import wavefront_cli.lib.auth



class Configure(Base):
    """authenticate the user's session"""

    def run(self):

        print "The configure command will overwrite the Wavefront URL and API Token stored in ~/.wavefront/credentials"
        wavefront_cli.lib.auth.do_auth(self.options)