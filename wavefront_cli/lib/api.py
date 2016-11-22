import requests
import sys
import auth
import requests

def clean_url(url):
    url = url
    if url.endswith("/api/"):
        url = url[:-5]
    elif url.endswith("/api"):
        url = url[:-4]
    elif url.endswith("/"):
        url = url[:-1]
    return url

def validate_token(url, token):
    url = clean_url(url)
    # /daemon/test?token=$TOKEN
    validate_url = "%s/api/daemon/test?token=%s" % (url, token)
    try:
        r = requests.post(validate_url)
        status_code = r.status_code
        if status_code == 401:
            print "Error validating token: Unauthorized. Make sure your Wavefront account has Agent Management permissions."
            return False
        elif status_code == 200:
            print "Successfully validated token."
            return True
        elif status_code == 400:
            print "Url not found. Please check that your Wavefront URL is valid and that this machine has http access."
            return False
    except:
        print "Error sending API Request. Are you sure your URL is correct? ", sys.exc_info()


def deploy_dashboard(db_json_url, wf_url, api_token):
    print "Deploying Dashboard with %s, %s, %s" % (db_json_url, wf_url, api_token)
    return True
