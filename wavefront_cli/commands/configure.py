"""The hello command."""


from json import dumps

from .base import Base

import wavefront.auth


class Configure(Base):
    """authenticate the user's session"""

    def run(self):
        #wavefront.auth.do_auth(self.options)
        print wavefront.auth.get_or_set_auth(self.options)