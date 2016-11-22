from wavefront_cli.lib import message

from .base import Base


class Example(Base):

    '''
    install() - The install() method installs the integration. Usually this means creating a Telegraf config file
    in /etc/telegraf/telegraf.d. See statsd.py for a simple example.
    '''
    def install(self):

        print "This is an example integration subclass"

        # call validate_options() if you need to validate what options were passed
        # before writing the config file to /etc/telegraf/telegraf.d
        self.validate_options()

        # options that were passed to the  CLI are available as a dictionary: self.options
        # Example:
        #   statsd_port = self.options["statsd_port"]
        #

        # if the integration is a telegraf plugin, write a config file to /etc/telegraf/telegraf.d
        # system.write_file("/etc/telegraf/telegraf.d/10-example.conf", "....")


        # finally, if the install was successful, return True. If it wasn't return False.
        return True

    '''
    remove() - The remove() method should remove the integration. usually this means removing
    the telegraf config file for this integration.
    '''
    def remove(self):

        # os.remove("/etc/telegraf/telegraf.d/10-example.conf")
        return True

    def validate_options(self):
        return True