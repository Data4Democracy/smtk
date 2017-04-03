import os
import facepy


def validate_auth_elements(auth):
    """Validates the authentication elements.

    Expects a list of authentication elements and returns it unchanged."""

    for credential in auth:
        if not isinstance(credential, str):
            raise RuntimeError(
                "credential must be string, got: %s" % (type(credential)))
        if len(credential) <= 0:
            raise RuntimeError('invalid credential %s' % (credential))

    return auth


def twitter_auth(consumer_key=None, consumer_secret=None, access_key=None, access_secret=None):
    """Validate and create a list of twitter authentication elements"""

    if not consumer_key:
        consumer_key = os.environ.get('T_CONSUMER_KEY', consumer_key)
    if not consumer_secret:
        consumer_secret = os.environ.get('T_CONSUMER_SECRET', consumer_secret)
    if not access_key:
        access_key = os.environ.get('T_ACCESS_KEY', access_key)
    if not access_secret:
        access_secret = os.environ.get('T_ACCESS_SECRET', access_secret)

    auth = [consumer_key, consumer_secret, access_key, access_secret]

    if validate_auth_elements(auth):

        return auth


def facebook_auth(auth):
    """Validate and create facebook access token"""
    if auth:
        app_id, app_secret, api_version = auth
    else:
        app_id, app_secret, api_version = None, None, '2.6'

    app_id = os.getenv('FB_APP_ID', app_id)
    app_secret = os.getenv('FB_APP_SECRET', app_secret)
    api_version = os.getenv('FB_API_VERSION', api_version)

    auth = [app_id, app_secret, api_version]

    if validate_auth_elements(auth):
        auth_token = facepy.utils.get_application_access_token(
            app_id, app_secret, api_version=api_version)
        print(auth_token)

        return (auth_token)
