

from .base import Base

class TestStatsD(Base):
    """Say hello, world!"""

    def install_config(self):
        print "Hello from TestStatsD install_config()"
        print self.options

    def install_dashboard(self):
        print "Hello from TestStatsD install_config()"
