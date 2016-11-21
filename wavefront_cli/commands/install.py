"""The proxy command."""
import sys

from wavefront_cli.lib import message

import wavefront_cli.lib.aws
import wavefront_cli.lib.api
import wavefront_cli.lib.proxy
import wavefront_cli.lib.agent

import wavefront_cli.integrations.wavefront
from wavefront_cli.integrations.statsd import StatsD
from wavefront_cli.integrations.wavefront import Wavefront

from .base import Base


class Install(Base):
    """Install the Wavefront Proxy."""

    def run(self):


        agent_name = "telegraf"

        message.print_welcome()
        '''
        wave install
            [--proxy]
                [--wavefront-url=<wavefront_url>]
                [--api-token=<api_token>]
            [--agent]
                [--proxy-address=<address>]
                [--proxy-port=<port>]
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

        # agent options
        agent = self.options.get('--agent')
        proxy_address = self.options.get('--proxy-address')
        proxy_port = self.options.get('--proxy-port')

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
            print "Beginning interactive installation..."
            prompt = True


        # figure out what they want to install
        if prompt:
            proxy_input = raw_input("Would you like to install the Wavefront Proxy on this host? (yes or no): \n").lower()
            if proxy_input == "y" or proxy_input == "yes":
                proxy = True
            agent_input = raw_input("Would you like to install Telegraf (metric collection agent) on this host? (yes or no): \n").lower()
            if agent_input == "y" or agent_input == "yes":
                agent = True
            statsd_input = raw_input("Would you like to configure StatsD integration on this host? (yes or no): \n").lower()
            if statsd_input:
                statsd = True

            # if this is an ec2 instance, ask if they would like to add ec2 metadata
            if wavefront_cli.lib.aws.is_ec2_instance():
                aws_input = raw_input("Would you like to add AWS EC2 Metadata to metrics from this host? (yes or no): \n").lower()
                if aws_input == "y" or agent_input == "yes":
                    aws = True

        if proxy:
            if not wavefront_url:
                wavefront_url = raw_input("Please enter the url to your Wavefront instance (default = https://try.wavefront.com): \n") or "https://try.wavefront.com"
            if not api_token:
                api_token = raw_input("Please enter a valid Wavefront API Token: \n")

            # Validate token first
            print "Validating API Token using Wavefront URL: ", wavefront_url

            if not wavefront_cli.lib.api.validate_token(wavefront_url, api_token):
                sys.exit(1)

            # Install Proxy
            if not wavefront_cli.lib.proxy.install_proxy():
                sys.exit(1)

            # Configure Proxy
            if not wavefront_cli.lib.proxy.configure_proxy(wavefront_url, api_token):
                sys.exit(1)


        if agent:
            if not proxy_address:
                proxy_address = raw_input("Please enter the address to your Wavefront proxy (default = localhost): \n") or "localhost"
            if not proxy_port:
                proxy_port = raw_input("Please enter the port of your Wavefront proxy (default = 2878): \n") or "2878"

            # Install Agent
            if not wavefront_cli.lib.agent.install_agent():
                sys.exit(1)

            # Configure Wavefront Integration
            wf_opts = {}
            wf_opts["proxy_address"] = proxy_address
            wf_opts["proxy_port"] = proxy_port
            wf = Wavefront(wf_opts)

            if wf.install():
                message.print_success("Successfully Installed Wavefront Integration!")
            else:
                message.print_warn("Failed during Wavefront Integration installation!")
                sys.exit(1)

            wavefront_cli.lib.system.restart_service(agent_name)
        # Integrations: agent must be restarted after installing an integration

        if aws:
            if not aws_region:
                aws_region = raw_input("Please enter the AWS region (example = us-west-2): \n")
            if not aws_secret_key_id:
                aws_secret_key_id = raw_input("Please enter your AWS IAM Access Key ID: \n")
            if not aws_secret_key:
                aws_secret_key = raw_input("Please enter your AWS IAM Secret Key: \n")

            if not wavefront_cli.lib.aws.tag_telegraf_config(aws_region, aws_secret_key_id, aws_secret_key):
                sys.exit(1)

            wavefront_cli.lib.system.restart_service(agent_name)


        if statsd:

            if not statsd_port:
                statsd_port = raw_input("Please enter the port you would like StatsD to listen on (default = 8125): \n") or "8125"

            # Install StatsD
            opts = {}
            opts["statsd_port"] = statsd_port
            int_statsd = StatsD(opts)
            if int_statsd.install():
                message.print_success("Successfully Installed StatsD Integration!")
            else:
                sys.exit(1)

            wavefront_cli.lib.system.restart_service(agent_name)

