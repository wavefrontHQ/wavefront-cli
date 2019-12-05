"""Wavefront API utility."""

from __future__ import print_function

import sys

import requests


def clean_url(url):
    """Convert user input URL to clean URL."""
    if url.endswith("/api/"):
        url = url[:-5]
    elif url.endswith("/api"):
        url = url[:-4]
    elif url.endswith("/"):
        url = url[:-1]
    return url


def validate_token(url, token):
    """Validate wavefront credential."""
    url = clean_url(url)
    # /daemon/test?token=$TOKEN
    validate_url = "%s/api/daemon/test?token=%s" % (url, token)
    is_valid = False
    try:
        response = requests.post(validate_url)
        status_code = response.status_code
        if status_code == 401:
            print("Error validating token: Unauthorized. Make sure your"
                  " Wavefront account has Agent Management permissions.")
        elif status_code == 200:
            print("Successfully validated token.")
            is_valid = True
        elif status_code == 400:
            print("Url not found. Please check that your Wavefront URL is"
                  " valid and that this machine has http access.")
    except requests.exceptions.RequestException:
        print("Error sending API Request. Are you sure your URL"
              " is correct? ", sys.exc_info())

    return is_valid


def deploy_dashboard(db_json_url, wf_url, api_token):
    """Deploy a dashboard in wavefront."""
    print("Deploying Dashboard with %s, %s, %s"
          % (db_json_url, wf_url, api_token))
    return True
