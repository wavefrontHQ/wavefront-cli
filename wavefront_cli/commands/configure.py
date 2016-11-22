"""The hello command."""

from .base import Base

from wavefront_cli.lib import auth



class Configure(Base):
    """authenticate the user's session"""

    def run(self):

        print "The configure command will overwrite the Wavefront URL and API Token stored in ~/.wavefront/credentials"
        auth.do_auth(self.options)