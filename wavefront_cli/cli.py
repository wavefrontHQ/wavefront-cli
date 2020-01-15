# pylint: disable=line-too-long
"""
wave.

Usage:
  wave install [--proxy] [--wavefront-url=<wavefront_url>] [--api-token=<api_token>] [--proxy-next] [--agent] [--proxy-address=<address>] [--proxy-port=<port>] [--agent-tags=<tags>] [--statsd] [--statsd-port=<statsd_port>] [--aws] [--aws-region=<aws_region>] [--aws-secret-key-id=<aws_secret_key_id>] [--aws-secret-key=<aws_secret_key]
  wave integration <name> (install|remove) [<option>...]
  wave configure [--wavefront-url=<wavefront_url>] [--api-token=<api_token>]
  wave -h | --help
  wave --version

Options:
  -h --help                             Show this screen.
  --version                             Show version.
  -u --wavefront-url <wavefront_url>    The URL to your Wavefront instance.
  -a --api-token <api_token>            Your Wavefront API Token.
  -p --proxy-address <address>          The Address of your Wavefront proxy.
  -P --proxy-port <proxy_port>          The port of your Wavefront proxy.
  --statsd-port=PORT                    The port that StatsD should listen on [default: 8125]
  --agent-tags <tags>                   A comma separated list of key value pairs i.e. env=dev,app=myapp

Examples:
  wave install --proxy --agent


Help:
  For help using the Wavefront client CLI, please visit:
  https://community.wavefront.com

"""  # noqa;
# pylint: enable=line-too-long

from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as version
from . import commands


def main():
    """CLI entry point for all the commands."""
    options = docopt(__doc__, version=version)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for key, value in options.items():
        if hasattr(commands, key) and value:
            # Don't call install while running integration command
            if key == 'install' and options.get('integration'):
                continue
            module = getattr(commands, key)
            wave_commands = getmembers(module, isclass)
            command = [command[1] for command in wave_commands if
                       command[0] != 'Base'][0]
            command = command(options)
            command.run()
