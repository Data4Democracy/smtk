import os
import facepy


def validate_auth_elements(auth):
    """Validates the authentication elements.

    Expects a list of authentication elements and returns it unchanged."""

    for credential in auth:
        if not isinstance(credential, str):
            print('credential must be string')
            return None
        if len(credential) <= 0:
            print('invalid credential {}'.format(credential))
            return None

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


def facebook_auth(app_id=None, app_secret=None, api_version=None):
    """Validate and create facebook access token"""

    if not app_id:
        app_id = os.environ.get('FB_APP_ID', app_id)
    if not app_secret:
        app_secret = os.environ.get('FB_APP_SECRET', app_secret)
    if not api_version:
        api_version = os.environ.get('FB_API_VERSION', api_version)

    auth = [app_id, app_secret, api_version]

    if validate_auth_elements(auth):
        auth_token = facepy.utils.get_application_access_token(*auth)

        return (auth_token[0], api_version)
