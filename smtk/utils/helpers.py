import os
import facepy


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

    for credential in auth:
        if not isinstance(credential, str):
            raise TypeError(
                "credential must be string, got: %s" % (type(credential)))
        if len(credential) <= 0:
            raise TypeError('invalid credential %s' % (credential))

    return auth


def facebook_auth(app_id=None, app_secret=None):
    """Validate and create facebook access token"""

    if not app_id:
        app_id = os.environ.get('FB_APP_ID', app_id)
    if not app_secret:
        app_secret = os.environ.get('FB_APP_SECRET', app_secret)

    auth = [app_id, app_secret]

    for credential in auth:
        if not isinstance(credential, str):
            raise TypeError(
                "credential must be string, got: %s" % (type(credential)))
        if len(credential) <= 0:
            raise TypeError('invalid credential %s' % (credential))

    auth_token = facepy.utils.get_application_access_token(*auth)

    return auth_token


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
            raise TypeError('invalid credential %s' % (credential))
        if len(credential) <= 0:
            raise TypeError('invalid credential %s' % (credential))

    return auth
