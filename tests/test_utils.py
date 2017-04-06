import pytest
import os
from smtk.utils import helpers

@pytest.fixture
def credentials():
    return ['p_consumer', 'pc_secret', 'p_access', 'pa_secret']


def test_twitter_auth_from_env_vars(monkeypatch):
    monkeypatch.setenv('T_CONSUMER_KEY', 'consumer')
    monkeypatch.setenv('T_CONSUMER_SECRET', 'c_secret')
    monkeypatch.setenv('T_ACCESS_KEY', 'access')
    monkeypatch.setenv('T_ACCESS_SECRET', 'a_secret')

    auth = helpers.twitter_auth()

    assert len(auth) == 4
    for credential in auth:
        assert credential in ['consumer', 'c_secret', 'access', 'a_secret']


def test_twitter_auth_from_parameters():
    auth = helpers.twitter_auth(
        'p_consumer', 'pc_secret', 'p_access', 'pa_secret')

    assert len(auth) == 4
    for cred in auth:
        assert cred in ['p_consumer', 'pc_secret', 'p_access', 'pa_secret']


def test_twitter_auth_invalid_parameters(monkeypatch):
    monkeypatch.setenv('T_CONSUMER_KEY', '')
    monkeypatch.setenv('T_CONSUMER_SECRET', '')
    monkeypatch.setenv('T_ACCESS_KEY', '')
    monkeypatch.setenv('T_ACCESS_SECRET', '')

    auth = helpers.twitter_auth()

    assert auth is None


def test_twitter_auth_invalid_type_parameters():
    auth = helpers.twitter_auth(10, 20, 30, 40)

    assert auth is None

def test_facebook_auth_from_env_vars(monkeypatch):
    auth = helpers.facebook_auth()

    assert len(auth) == 2
    assert os.environ['FB_APP_ID'] in auth[0]

def test_facebook_auth_from_param_list():
    FB_APP_ID = os.environ['FB_APP_ID']
    FB_APP_SECRET = os.environ['FB_APP_SECRET']
    auth = helpers.facebook_auth(auth=[FB_APP_ID,FB_APP_SECRET])

    assert len(auth) == 2
    assert FB_APP_ID in auth[0]
