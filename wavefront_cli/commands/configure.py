"""The hello command."""

# pylint: disable=R0903


from .base import Base
from ..lib import auth


class Configure(Base):
    """authenticate the user's session."""

    def run(self):
        """Override Wavefront Credentials."""
        print("The configure command will overwrite the Wavefront URL"
              " and API Token stored in ~/.wavefront/credentials")
        auth.do_auth(self.options)
