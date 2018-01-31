
import os
from wavefront_cli.lib import message
from wavefront_cli.lib import system
from .base import Base



class Wavefront(Base):

    conf_path = "/etc/telegraf/telegraf.d/10-wavefront.conf"
    conf = """
    # # Configuration for Wavefront proxy to send metrics to
    [[outputs.wavefront]]
    # prefix = "telegraf."
      host = "%s"
      port = %s
      metric_separator = "."
      source_override = ["hostname", "agent_host", "node_host"]
      convert_paths = true
      use_regex = false
        """

    def install(self):

        if not self.validate_options():
            return False

        proxy_address = self.options["proxy_address"]
        proxy_port = self.options["proxy_port"]

        out = self.conf % (proxy_address, proxy_port)

        if system.write_file(self.conf_path, out):
            message.print_success("Wrote Wavefront configuration to " + self.conf_path)
        else:
            message.print_warn("Failed writing config file to %s - do you have write permission on this location?" % (self.conf_path))
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

    def validate_options(self):
        if not self.options['proxy_address']:
            message.print_warn("Missing required option: proxy_address")
            return False
        if not self.options['proxy_port']:
            # default to 2878
            self.options['proxy_port'] = 2878
        return True
