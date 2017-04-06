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


def facebook_auth(auth=None):
    """Validate and create facebook access token"""
    if auth:
        app_id, app_secret = auth
    else:
        app_id, app_secret = None, None

    app_id = os.getenv('FB_APP_ID', app_id)
    app_secret = os.getenv('FB_APP_SECRET', app_secret)

    auth = [app_id, app_secret]

    if validate_auth_elements(auth):
        auth_token = facepy.utils.get_application_access_token(
            app_id, app_secret)

        return (auth_token)


def reddit_auth(client_id=None, client_secret=None):
    """Validate and create reddit access credentials"""
    if not client_id:
        client_id = os.environ.get('R_CLIENT_ID', client_id)
    if not client_secret:
        client_secret = os.environ.get('R_CLIENT_SECRET', client_secret)

    user_agent = 'smtk:d4d'
    # auth = [client_id, client_secret, user_agent]
    auth = dict(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    for credential in auth.values():
        if not isinstance(credential, str):
            print('credential must be string')
            return None
        if len(credential) <= 0:
            print('invalid credential {}'.format(credential))
            return None

    return auth
