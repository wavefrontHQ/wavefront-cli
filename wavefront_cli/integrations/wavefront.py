import os
from wavefront_cli.lib import message
from wavefront_cli.lib import system
from .base import Base



class Wavefront(Base):
    """Say hello, world!"""

    conf_path = "/etc/telegraf/telegraf.d/10-wavefront.conf"
    conf = """
    # # Configuration for Wavefront proxy to send metrics to
    [[outputs.wavefront]]
    # prefix = "telegraf."
      host = "%s"
      port = %s
      metric_separator = "."
      convert_paths = true
      use_regex = false
        """

    def install(self):

        proxy_address = self.options["proxy_address"]
        proxy_port = self.options["proxy_port"]

        out = self.conf % (proxy_address, proxy_port)
        if system.write_file(self.conf_path, out):
            message.print_success("Wrote Wavefront configuration to " + self.conf_path)
        else:
            message.print_warn("Failed configuring Wavefront integration!")
            return False

        return True

    def remove(self):
        try:
            os.remove(self.conf_path)
            message.print_success("Remove Wavefront configuration file " + self.conf_path)
        except:
            message.print_warn("Unable to remove conf file at: " + self.conf_path)
            message.print_warn("Was Wavefront integration already removed?")
            return False

        return True
