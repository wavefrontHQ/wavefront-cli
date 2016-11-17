"""The proxy command."""
from json import dumps
from .base import Base
# wavefront API functions
import wavefront.auth
import wavefront.api
import wavefront.system
import wavefront.proxy
import wavefront.agent
import wavefront.message
import wavefront.aws

import subprocess
import json
import os
import sys
import platform

class Install(Base):
    """Install the Wavefront Proxy."""

    def run(self):

        wavefront.aws.get_instance_id()

        wavefront.message.print_welcome()
        '''
        wave install
            [--proxy]
                [--wavefront-url=<wavefront_url>]
                [--api-token=<api_token>]
            [--agent]
                [--proxy-address=<address>]
                [--proxy-port=<port>]
            [--aws-ec2-tags]
                [--aws-region=<aws_region>]
                [--aws-secret-key-id=<aws_secret_key_id>]
                [--aws-secret-key=<aws_secret_key]
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
        aws = self.options.get('--aws-ec2-tags')
        aws_region = self.options.get('--aws-region')
        aws_secret_key_id = self.options.get('--aws-secret-key-id')
        aws_secret_key = self.options.get('--aws-secret-key')

        prompt = False
        if not proxy and not agent and not aws:
            print "Beginning interactive installation..."
            prompt = True


        # figure out what they want to install
        if prompt:
            proxy_input = raw_input("Would you like to install the Wavefront Proxy on this host? (yes or no): \n").lower()
            if proxy_input == "y" or proxy_input == "yes":
                proxy = True
            agent_input = raw_input("Would you like to install the Telegraf agent on this host? (yes or no): \n").lower()
            if agent_input == "y" or agent_input == "yes":
                agent = True
            # if this is an ec2 instance, ask if they would like to add ec2 metadata
            if wavefront.aws.is_ec2_instance():
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
            valid = wavefront.api.validate_token(wavefront_url,api_token)
            if not wavefront.api.validate_token(wavefront_url,api_token):
                sys.exit(1)

            # Install Proxy
            if not wavefront.proxy.install_proxy():
                sys.exit(1)

            # Configure Proxy
            if not wavefront.proxy.configure_proxy(wavefront_url,api_token):
                sys.exit(1)


        if agent:
            if not proxy_address:
                proxy_address = raw_input("Please enter the address to your Wavefront proxy (default = localhost): \n") or "localhost"
            if not proxy_port:
                proxy_port = raw_input("Please enter the port of your Wavefront proxy (default = 2878): \n") or "2878"

            # Install Agent
            if not wavefront.agent.install_agent():
                sys.exit(1)

            if not wavefront.agent.configure_agent(proxy_address,proxy_port):
                sys.exit(1)

        if aws:
            if not aws_region:
                aws_region = raw_input("Please enter the AWS region (example = us-west-2): \n")
            if not aws_secret_key_id:
                aws_secret_key_id = raw_input("Please enter your AWS IAM Access Key ID: \n")
            if not aws_secret_key:
                aws_secret_key = raw_input("Please enter your AWS IAM Secret Key: \n")

            if not wavefront.aws.tag_telegraf_config(aws_region, aws_secret_key_id, aws_secret_key):
                sys.exit(1)



