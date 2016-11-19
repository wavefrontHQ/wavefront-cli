from .. import system
from .. import message

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


def configure(statsd_port="8125"):

    message.print_bold("Configuring StatsD Integration!")

    out = conf % (statsd_port)
    if system.write_file(conf_path,out):
        message.print_success("Finished Configuring StatsD Integration!")
        return True
    else:
        message.print_warn("Failed Configuring StatsD Integration!")
        return False