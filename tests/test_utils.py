import pytest
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
    with pytest.raises(TypeError):
        helpers.twitter_auth()


def test_twitter_auth_invalid_type_parameters():
    with pytest.raises(TypeError):
        helpers.twitter_auth(10, 20, 30, 40)


def test_reddit_auth_invalid_type_parameters():
    with pytest.raises(TypeError):
        helpers.reddit_auth(10, 20)


def test_reddit_auth_invalid_parameters(monkeypatch):
    monkeypatch.setenv('R_CLIENT_ID', '')
    monkeypatch.setenv('R_CLIENT_SECRET', '')
    with pytest.raises(TypeError):
        helpers.reddit_auth(10, 20)
