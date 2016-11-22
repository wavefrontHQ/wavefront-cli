import subprocess
from wavefront_cli.lib import auth
from wavefront_cli.lib import message

class Base(object):
    """A base command."""

    def __init__(self, options):
        creds = auth.get_or_set_auth({})
        '''
        "user_url": user_url,
        "user_token": user_token
        '''
        self.wavefront_url = creds['user_url']
        self.api_token = creds['user_token']
        self.options = options

        cmd = "sudo mkdir -p /etc/telegraf/telegraf.d"
        ret_code = subprocess.call(cmd, shell=True)
        if ret_code > 0:
            message.print_warn("Unable to create integrations config directory at /etc/telegraf/telegraf.d")

    def validate_options(self):
        raise NotImplementedError('You must implement the validate_options() method!')

    def install(self):
        raise NotImplementedError('You must implement the install() method!')

    def remove(self):
        raise NotImplementedError("YOu must implement the remove() method!")

