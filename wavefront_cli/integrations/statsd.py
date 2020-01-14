"""This class manages(Install/Remove) the StatsD input plugin."""

import os

from .base import Base
from ..lib import message
from ..lib import system


class StatsD(Base):
    """Manage StatsD input plugin."""

    conf_path = "/etc/telegraf/telegraf.d/10-statsd.conf"
    conf = """
[[inputs.statsd]]
  ## Address and port to host UDP listener on
  service_address = ":%s"
  ## Delete gauges every interval (default=false)
  delete_gauges = false
  ## Delete counters every interval (default=false)
  delete_counters = false
  ## Delete sets every interval (default=false)
  delete_sets = false
  ## Delete timings & histograms every interval (default=true)
  delete_timings = true
  ## Percentiles to calculate for timing & histogram stats
  percentiles = [90]

  ## separator to use between elements of a statsd metric
  metric_separator = "_"

  ## Parses tags in the datadog statsd format
  ## http://docs.datadoghq.com/guides/dogstatsd/
  parse_data_dog_tags = false

  ## Statsd data translation templates, more info can be read here:
  ## https://github.com/influxdata/telegraf/blob/master/docs/DATA_FORMATS_INPUT.md#graphite
  # templates = [
  #     "cpu.* measurement*"
  # ]

  ## Number of UDP messages allowed to queue up, once filled,
  ## the statsd server will start dropping packets
  allowed_pending_messages = 10000

  ## Number of timing/histogram values to track per-measurement in the
  ## calculation of percentiles. Raising this limit increases the accuracy
  ## of percentiles but also increases the memory usage and cpu time.
  percentile_limit = 1000
           """

    def install(self):
        """Install StatsD input plugin."""
        self.validate_options()

        statsd_port = self.options["statsd_port"]

        out = self.conf % (statsd_port)
        if system.write_file(self.conf_path, out):
            message.print_success("Wrote StatsD service plugin configuration"
                                  " to %s" % (self.conf_path))
        else:
            message.print_warn("Failed writing config file to %s - do you"
                               " have write permission on this location?"
                               % self.conf_path)
            return False
        return True

    def remove(self):
        """Remove StatsD input plugin."""
        try:
            os.remove(self.conf_path)
            message.print_success("Removed StatsD configuration file "
                                  + self.conf_path)
        except OSError:
            message.print_warn("Unable to remove conf file at: "
                               + self.conf_path)
            message.print_warn("Was StatsD integration already removed?")
            return False

        return True

    def validate_options(self):
        """Validate required parameter for StatsD input plugin."""
        if not self.options and not self.options['statsd_port']:
            # default value
            self.options['statsd_port'] = "8125"
        return True
