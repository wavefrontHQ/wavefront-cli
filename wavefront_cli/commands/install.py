"""The proxy command."""
# pylint: skip-file

from __future__ import print_function

import sys

from wavefront_cli import lib
from wavefront_cli.integrations.statsd import StatsD
from wavefront_cli.integrations.wavefront import Wavefront

from .base import Base

try:
    input = raw_input
except NameError:
    pass


class Install(Base):
    """Manage agent installation."""

    def run(self):
        """Install wavefront proxy/statsd/telegraf."""
        agent_name = "telegraf"
        lib.message.print_welcome()
        '''
        wave install
            [--proxy]
                [--wavefront-url=<wavefront_url>]
                [--api-token=<api_token>]
                [--proxy-next]
            [--agent]
                [--proxy-address=<address>]
                [--proxy-port=<port>]
                [--agent-tags=<tags>]
            [--aws]
                [--aws-region=<aws_region>]
                [--aws-secret-key-id=<aws_secret_key_id>]
                [--aws-secret-key=<aws_secret_key]
            [--statsd]
                [--statsd-port=<statsd_port>]
        '''

        # proxy options
        proxy = self.options.get('--proxy')
        wavefront_url = self.options.get('--wavefront-url')
        api_token = self.options.get('--api-token')
        proxy_next = self.options.get('--proxy-next')

        # agent options
        agent = self.options.get('--agent')
        proxy_address = self.options.get('--proxy-address')
        proxy_port = self.options.get('--proxy-port')
        agent_tags = self.options.get('--agent-tags')

        # aws options
        aws = self.options.get('--aws')
        aws_region = self.options.get('--aws-region')
        aws_secret_key_id = self.options.get('--aws-secret-key-id')
        aws_secret_key = self.options.get('--aws-secret-key')

        # statsd options
        statsd = self.options.get('--statsd')
        statsd_port = self.options.get('--statsd-port')

        # Decide when we want to prompt or not.
        prompt = False
        if not proxy and not agent and not aws and not statsd:
            print("Beginning interactive installation...")
            prompt = True

        # figure out what they want to install
        if prompt:
            proxy_input = input("Would you like to install the Wavefront Proxy"
                                " on this host? (yes or no)"
                                " [default: no]: \n").lower()
            if proxy_input == "y" or proxy_input == "yes":
                proxy = True
            else:
                proxy = False

            agent_input = input("Would you like to install Telegraf (metric"
                                " collection agent) on this host? (yes or no)"
                                " [default: no]: \n").lower()
            if agent_input == "y" or agent_input == "yes":
                agent = True
                agent_tags = input('Please enter a comma separated list of'
                                   ' tags you would like added to metrics'
                                   ' from this Telegraf host'
                                   ' ("env=dev,app=myapp") or press Enter'
                                   ' to continue without adding any tags: \n')
            else:
                agent = False
            statsd_input = input("Would you like to configure StatsD"
                                 " integration on this host? (yes or no)"
                                 " [default: no]: \n").lower()
            if statsd_input == "y" or statsd_input == "yes":
                statsd = True
            else:
                statsd = False

            # if this is an ec2 instance, ask if they would like
            # to add ec2 metadata
            if lib.aws.is_ec2_instance():
                aws_input = input("Would you like to add AWS EC2 Metadata to "
                                  "metrics from this host? (yes or no)"
                                  " [default: no]: \n").lower()
                if aws_input == "y" or aws_input == "yes":
                    aws = True
                else:
                    aws = False

        if proxy:
            if not wavefront_url:
                wavefront_url = input("Please enter the url to your Wavefront"
                                      " instance (default = "
                                      "https://try.wavefront.com): \n")\
                                or "https://try.wavefront.com"
            if not api_token:
                api_token = input("Please enter a valid Wavefront"
                                  " API Token: \n")

            # Validate token first
            print("Validating API Token using Wavefront URL: ", wavefront_url)

            if not lib.api.validate_token(wavefront_url, api_token):
                sys.exit(1)

            lib.auth.save_auth(wavefront_url, api_token)
            # Install Proxy
            if not lib.proxy.install_proxy(proxy_next):
                sys.exit(1)

            # Configure Proxy
            if not lib.proxy.configure_proxy(wavefront_url, api_token):
                sys.exit(1)

        if agent:
            # required agent options
            if not proxy_address:
                proxy_address = input("Please enter the address to your"
                                      " Wavefront proxy (default = "
                                      "localhost): \n") or "localhost"
            if not proxy_port:
                proxy_port = input("Please enter the port of your"
                                   " Wavefront proxy (default = 2878): \n")\
                             or "2878"

            # Install the Wf integration first (Telegraf won't start
            # if an output plugin is not already created
            # Configure Wavefront Integration
            wf_opts = {}
            wf_opts["proxy_address"] = proxy_address
            wf_opts["proxy_port"] = proxy_port
            wf = Wavefront("Wavefront", wf_opts)

            if wf.install():
                lib.message.print_success("Successfully Installed"
                                          " Wavefront Integration!")
            else:
                lib.message.print_warn("Failed during Wavefront"
                                       " Integration installation!")
                sys.exit(1)

            # Now it is safe to install the agent
            if not lib.agent.install_agent():
                sys.exit(1)

            if agent_tags:
                tags = lib.util.cskv_to_dict(agent_tags)
                if not lib.agent.tag_telegraf_config('cli user tags', tags):
                    sys.exit(1)

            lib.system.restart_service(agent_name)

        # Integrations: agent must be restarted after installing an integration

        if aws:
            if not aws_region:
                aws_region = input("Please enter the AWS region"
                                   " (example = us-west-2): \n")
            if not aws_secret_key_id:
                aws_secret_key_id = input("Please enter your AWS"
                                          " IAM Access Key ID: \n")
            if not aws_secret_key:
                aws_secret_key = input("Please enter your AWS IAM"
                                       " Secret Key: \n")

            if not lib.aws.tag_telegraf_config(aws_region,
                                               aws_secret_key_id,
                                               aws_secret_key):
                sys.exit(1)

            lib.system.restart_service(agent_name)

        if statsd:
            if not statsd_port:
                statsd_port = input("Please enter the port you would like"
                                    " StatsD to listen on"
                                    " (default = 8125): \n") or "8125"

            # Install StatsD
            opts = {}
            opts["statsd_port"] = statsd_port
            int_statsd = StatsD("StatsD", opts)
            if int_statsd.install():
                lib.message.print_success("Successfully Installed"
                                          " StatsD Integration!")
            else:
                sys.exit(1)

            lib.system.restart_service(agent_name)
