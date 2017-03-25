import twitter
from smtk.utils import helpers


def setup_api(consumer_key=None, consumer_secret=None, access_key=None, access_secret=None):
    auth = helpers.twitter_auth(
        consumer_key, consumer_secret, access_key, access_secret)
    api = twitter.Api(*auth)
    return api


def get_profiles(api):
    profiles = api.UsersLookup(include_entities=False, user_id=user_ids)
    return profiles


def get_friends(api, screen_name):
    friends = api.GetFriendIDsPaged(
        screen_name=screen_name, cursor=cursor, count=5000)
    return friends


def get_followers(api):
    followers = api.GetFollowerIDsPaged(screen_name=screen_name, count=5000)
    return followers


def get_tweets(api):
    tweets = api.GetUserTimeline(**kwargs)
    return tweets
