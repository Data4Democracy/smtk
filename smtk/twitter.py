import twitter
from smtk.utils import helpers


class CollectTwitter:
    """Sets up a twitter collection. 
    
    Inherit from on_tweet, on_profile, on_start to handle stream of data
    returned by a running collection.
    """

    def __init__(self, *auth):
        self.auth = helpers.twitter_auth(auth)

    def on_tweet(self):
        """ Called when tweet is found"""
        pass

    def on_profile(self):
        """Called when profile is found"""

    def on_start(self):
        """Called when collection is started
        
        Inherit from CollectTwitter class to override to create """
        # verify credentials

    def get_friends(self):
        # accepts seed user(s) as list
        # gather list of friends
        # config option : all profiles or only seeds
        # config option : create connection
        # returns list of IDs
        # see https://github.com/Data4Democracy/collect-social/blob/master/collect_social/twitter/get_friends.py
        pass

    def get_followers(self):
        # same as get friends except for followers
        # returns list of IDs
        pass

    def get_profiles(self):
        # accepts profile(s) to gather as list of IDs or SN
        # calls on_profile
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/twitter/get_profiles.py
        pass

    def get_tweets(self):
        # accepts list of profiles
        # return calls on_tweet for each tweet found
        # config options: # tweets per profile
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/twitter/get_tweets.py
        pass


class StreamTwitter():
    """Stream twitter"""
    # TODO decide use tweepy/build from scratch/add to python-twitter