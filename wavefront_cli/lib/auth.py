"""Class to manage the wavefront authentication."""

import os
from os.path import expanduser

from . import api


WF_URL_ENVKEY = "WAVEFRONT_URL"
WF_TOKEN_ENVKEY = "WAVEFRONT_TOKEN"


def do_auth(options):
    """Store wavefront credential."""
    try:
        input = raw_input  # pylint: disable=redefined-builtin
    except NameError:
        pass

    if options and options['--wavefront-url']:
        user_url = options['--wavefront-url']
    else:
        user_url = input("Please enter your Wavefront URL: ")

    if options and options['--api-token']:
        user_token = options['--api-token']
    else:
        user_token = input("Please enter your Wavefront API Token: ")

    save_auth(user_url, user_token)


def save_auth(user_url, user_token):
    """Validate and Store wavefront credential."""
    home = expanduser("~") + "/.wavefront/"
    # make sure the wavefront home directory exists
    if not os.path.exists(home):
        os.makedirs(home)

    # validate the user's info
    valid = api.validate_token(user_url, user_token)
    if valid:
        creds = open(home + "credentials", "w")
        creds.write("%s\n%s" % (user_url, user_token))
        creds.close()
    return valid


def get_or_set_auth(options):
    """Manage wavefront credentials."""
    # did the user pass options?
    if options and options['--wavefront-url'] and options['--api-token']:
        # yes, save auth
        save_auth(options['--wavefront-url'], options['--api-token'])
        credential = get_auth()
    else:
        # the user didn't pass options, are there existing creds saved?
        creds = get_auth()
        if creds is not None:
            credential = creds
        else:
            do_auth(options)
            credential = get_auth()
    return credential


def get_auth():
    """Retrieve and validate already saved wavefront credentials."""
    try:
        home = expanduser("~") + "/.wavefront/"
        creds = open(home + "credentials", "r")
        text = creds.read()
        user_url = text.split("\n")[0]
        user_token = text.split("\n")[1]
        if api.validate_token(user_url, user_token):
            return {
                "user_url": user_url,
                "user_token": user_token
            }

        print("Your previously saved API Token failed to validate."
              " Was it deactivated?")
        return None
    except (OSError, IOError):
        return None
