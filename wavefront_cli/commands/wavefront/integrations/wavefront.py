
from .. import system
from .. import message

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


def configure(proxy_address, proxy_port):

    message.print_bold("Configuring Wavefront Integration!")

    out = conf % (proxy_address, proxy_port)
    if system.write_file(conf_path,out):
        message.print_success("Finished Configuring Wavefront Integration!")
        return True
    else:
        message.print_warn("Failed Configuring Wavefront Integration!")
        return False
