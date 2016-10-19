"""The hello command."""


from json import dumps

from .base import Base

import wavefront.auth


class Configure(Base):
    """authenticate the user's session"""

    def run(self):

        print "The configure command will overwrite the Wavefront URL and API Token stored in ~/.wavefront/credentials"
        wavefront.auth.do_auth(self.options)