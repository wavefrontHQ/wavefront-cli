"""The proxy command."""

from __future__ import print_function

import os
import pwd
import sys
import time

from wavefront_cli import lib
from wavefront_cli.integrations.statsd import StatsD
from wavefront_cli.integrations.wavefront import Wavefront

from .base import Base

try:
    input = raw_input  # pylint: disable=invalid-name,redefined-builtin
except NameError:
    pass


class Install(Base):  # pylint: disable=too-few-public-methods
    """Manage agent installation."""

    def run(self):
        """Install wavefront proxy/statsd/telegraf."""
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        agent_name = "telegraf"
        lib.message.print_welcome()
        # pylint: disable=pointless-string-statement
        '''
        wave install
            [--proxy]
                [--wavefront-url=<wavefront_url>]
                [--api-token=<api_token>]
                [--csp-api-token=<csp_api_token>]
                [--csp-app-id=<csp_app_id>]
                [--csp-app-secret=<csp_app_secret>]
                [--csp-org-id=<csp_org_id>]
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
        wavefront_api_token = self.options.get('--api-token')
        csp_api_token = self.options.get('--csp-api-token')
        csp_app_id = self.options.get('--csp-app-id')
        csp_app_secret = self.options.get('--csp-app-secret')
        csp_org_id = self.options.get('--csp-org-id')
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

            proxy = bool(proxy_input.lower() in ("y", "yes"))

            agent_input = input("Would you like to install Telegraf (metric"
                                " collection agent) on this host? (yes or no)"
                                " [default: no]: \n").lower()
            if agent_input.lower() in ("y", "yes"):
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
            statsd = bool(statsd_input.lower() in ("y", "yes"))

            # if this is an ec2 instance, ask if they would like
            # to add ec2 metadata
            if lib.aws.is_ec2_instance():
                aws_input = input("Would you like to add AWS EC2 Metadata to "
                                  "metrics from this host? (yes or no)"
                                  " [default: no]: \n").lower()
                aws = bool(aws_input.lower() in ("y", "yes"))

        if proxy:
            if not wavefront_url:
                wavefront_url = input("Please enter the url to your Wavefront"
                                      " instance (default = "
                                      "https://try.wavefront.com): \n") \
                                or "https://try.wavefront.com"

            auth_type = False
            if csp_org_id and csp_app_id and csp_app_secret:
                auth_type = True
            elif csp_api_token:
                auth_type = True
            elif wavefront_api_token:
                auth_type = True
                print("Validating API Token using Wavefront URL: ",
                      wavefront_url)
                if not lib.api.validate_token(wavefront_url,
                                              wavefront_api_token):
                    sys.exit(1)
                lib.auth.save_auth(wavefront_url, wavefront_api_token)

            if not auth_type:
                print("Error: Invalid combination of parameters.")
                sys.exit(1)

            # Install Proxy
            if not lib.proxy.install_proxy(proxy_next):
                sys.exit(1)

            if csp_org_id and csp_app_id and csp_app_secret:
                lib.configure_csp_oauth_options()
                lib.comment_auth_methods(csp_api_token=True,
                                         csp_oauth_app=False,
                                         wavefront_api_token=True)
            elif csp_api_token:
                lib.configure_csp_api_token_options()
                lib.comment_auth_methods(csp_api_token=False,
                                         csp_oauth_app=True,
                                         wavefront_api_token=True)
            elif wavefront_api_token:
                lib.configure_wavefront_api_token_options()
                lib.comment_auth_methods(csp_api_token=True,
                                         csp_oauth_app=True,
                                         wavefront_api_token=False)

            # Configure Proxy
            if not lib.proxy.configure_proxy(wavefront_url,
                                             wavefront_api_token,
                                             csp_api_token,
                                             csp_app_id,
                                             csp_app_secret,
                                             csp_org_id):
                sys.exit(1)

        if agent:
            # required agent options
            if not proxy_address:
                proxy_address = input("Please enter the address to your"
                                      " Wavefront proxy (default = "
                                      "localhost): \n") or "localhost"
            if not proxy_port:
                proxy_port = input("Please enter the port of your"
                                   " Wavefront proxy (default = 2878): \n") \
                             or "2878"

            # Install the Wf integration first (Telegraf won't start
            # if an output plugin is not already created
            # Configure Wavefront Integration
            wf_opts = {}
            wf_opts["proxy_address"] = proxy_address
            wf_opts["proxy_port"] = proxy_port
            wavefront_integration = Wavefront("Wavefront", wf_opts)

            if wavefront_integration.install():
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

            # check if user 'telegraf' has read permission for config path if
            # not change owner of telegraf path to 'telegraf' user recursively
            uid = pwd.getpwnam(agent_name).pw_uid
            path = '/etc/telegraf'

            if not uid == os.stat(path).st_uid:
                os.chown(path, uid, -1)
                for root, dirs, files in os.walk(path):
                    for name in dirs:
                        os.chown(os.path.join(root, name), uid, -1)
                    for name in files:
                        os.chown(os.path.join(root, name), uid, -1)
            # The static sleep is added for `os.chown` to change owner of
            # telegraf sub-directories and files
            time.sleep(5)

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
