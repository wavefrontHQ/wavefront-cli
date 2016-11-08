"""
wave

Usage:
  wave oli [--proxy] [--wavefront-url=<wavefront_url>] [--api-token=<api_token>] [--agent] [--proxy-address=<address>] [--proxy-port=<port>]
  wave configure [--wavefront-url=<wavefront_url>] [--api-token=<api_token>]
  wave proxy (install|remove)
  wave agent (install|remove) [--proxy-address=<address>] [--proxy-port=<port>]
  wave -h | --help
  wave --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -u --wavefront-url <wavefront_url>                The URL to your Wavefront instance.
  -a --api-token <api_token>                    Your Wavefront API Token.
  -p --proxy-address <address>                The Address of your Wavefront proxy.
  -P --proxy-port <proxy_port>                   The port of your Wavefront proxy.

Examples:
  wave proxy --wavefront-url=https://try.wavefront.com --api-token=YOUR_API_TOKEN
  wave agent --proxy-address=localhost --proxy-port=4242


Help:
  For help using the Wavefront client CLI, please visit:
  https://community.wavefront.com
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for k, v in options.iteritems():
        if hasattr(commands, k) and v:
            module = getattr(commands, k)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
