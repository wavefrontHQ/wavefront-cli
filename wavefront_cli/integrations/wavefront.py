from wavefront_cli.lib import message
from wavefront_cli.lib import system
from .base import Base


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



class Wavefront(Base):
    """Say hello, world!"""

    def install_config(self):

        proxy_address = self.options["proxy_address"]
        proxy_port = self.options["proxy_port"]

        out = conf % (proxy_address, proxy_port)
        if system.write_file(conf_path, out):
            return True
        else:
            message.print_warn("Failed Configuring Wavefront Integration!")
            return False

    def install_dashboard(self):
        pass


'''
    def configure(proxy_address, proxy_port):

        message.print_bold("Configuring Wavefront Integration!")

        out = conf % (proxy_address, proxy_port)
        if system.write_file(conf_path, out):
            message.print_success("Finished Configuring Wavefront Integration!")
            return True
        else:
            message.print_warn("Failed Configuring Wavefront Integration!")
            return False
'''