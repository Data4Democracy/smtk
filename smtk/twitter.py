from __future__ import absolute_import

import twitter

import smtk.utils.logger as l
from smtk.utils import helpers

# twitter.py conflicts with python-twitter library
# TODO thoughts: naming get_* vs gather_* vs collect_*
# TODO thoughts: get_x_by_screen_name / get_x_by_ids repetitive, support
# both? handle another way?


class CollectTwitter:
    """Sets up a twitter collection.
    Inherit from on_tweet, on_profile, on_start to handle stream of data
    returned by a running collection.
    """

    def __init__(self, stream=True):
        self.auth = helpers.twitter_auth()
        self.api = twitter.Api(*self.auth)
        self.stream = stream

    def on_tweet(self, tweet):
        """ Called when tweet is found"""
        # l.INFO("TWEET FOUND: {}".format(tweet.text))
        pass

    def on_profile(self, profile):
        """Called when profile is found"""
        l.INFO(profile)

    def on_start(self):
        """Called when collection is started
        Inherit from CollectTwitter class to override to create """
        pass

    def on_connection(self, account, connection, type_):
        """Called when connection is found"""
        # l.INFO("{} found {} with {}".format(type_, account, connection))
        pass

    def get_friends(self, ids=None, screen_names=None, request_limit=3):
        """In context of twitter friends are accounts the source is following"""
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/twitter/get_friends.py
        if ids is None:
            ids = []

        if not screen_names is None:
            ids += self._screen_names_to_ids(screen_names)

        for id_ in ids:
            self._stream_friends_by_id(id_, request_limit=3)

    def get_followers(self, ids=None, screen_names=None, request_limit=3, on_conneciton=True):
        # TODO on_connection? Param to return connections or always do it?
        if ids is None:
            ids = []

        if not screen_names is None:
            ids += self._screen_names_to_ids(screen_names)

        for id_ in ids:
            self._stream_followers_by_id(id_, request_limit=3)

    def get_profiles(self, ids=None, stream=True):
        # TODO profiles by screen_name
        # TODO Deal with timeouts

        lookup = []
        remain = len(ids)
        profiles = []
        for id_ in ids:
            lookup.append(id_)
            if len(lookup) >= 100:
                # limit 100 profiles per request
                chunk = self._fetch_users_by_id(ids=lookup, stream=stream)
                remain -= len(lookup)
                l.INFO("""
                       Fetching {lookup} profiles. {remain} remain
                       """.format(lookup, remain))
                profiles += chunk
        profiles += self._fetch_users_by_id(ids=lookup, stream=stream)
        l.INFO("Fetching remaining %s profile(s)" % (len(lookup)))

        return profiles

    def get_tweets(self, ids=None, screen_names=None, limit=3200):
        if ids is None:
            ids = []

        if not screen_names is None:
            ids += self._screen_names_to_ids(screen_names)

        l.INFO("Getting tweets for ids: %s" % (ids))
        for id_ in ids:
            self._stream_tweets_by_user_id(id_, limit=limit)

    def _fetch_users_by_id(self, ids=None, stream=True):
        if len(ids) > 100:
            raise RuntimeError("Too many users to fetch, got: %s" % (len(ids)))

        profiles = self.api.UsersLookup(user_id=ids,
                                        include_entities=False)
        if stream:
            for profile in profiles:
                self.on_profile(profile)
        return profiles

    def _fetch_profiles_by_screen_name(self, screen_name):
        return self.api.UsersLookup(screen_name=screen_name)

    def _fetch_profiles_by_screen_names(self, screen_names):
        return [
            self.api.UsersLookup(screen_name=[screen_name])
            for screen_name in screen_names
        ]

    def _screen_names_to_ids(self, screen_names):
        ids = []
        lookups = self._fetch_profiles_by_screen_names(screen_names)
        for lookup in lookups:
            for user in lookup:
                ids.append(user.id)
        return ids

    def _stream_tweets_by_user_id(self, id_, **kwargs):
        # TODO rework this to use min/max tweets instead of assuming < 200
        # means done
        kwargs = dict(
            user_id=id_,
            count=200
        )

        # TODO consider breaking up/refactoring
        while True:
            try:
                l.INFO("Fetching 200 tweets %s" % (kwargs))
                tweets = self.api.GetUserTimeline(**kwargs)

            except Exception as e:
                l.WARN("%s kwargs %s" % (e, kwargs))
                return None

            l.INFO("Streaming tweets")
            for tweet in tweets:
                self.on_tweet(tweet)

            if len(tweets) < 200:
                # TODO Fix - Using <200 as proxy for end of user timeline
                l.INFO("Stream ended < 200 tweets")
                break

            tweet_ids = [tweet.id for tweet in tweets]
            if len(tweet_ids) > 0:
                # Next request start at oldest tweet in current request
                l.INFO("Setting max ID: {}".format(min(tweet_ids)))
                kwargs['max_id'] = min(tweet_ids)

    def _stream_tweets_by_screen_name(self, screen_name):
        user = self._fetch_profiles_by_screen_name(screen_name=screen_name)
        return self._stream_friends_by_id(self, user.id)

    def _stream_friends_by_id(self, user_id, request_limit=3):
        kwargs = dict(
            user_id=user_id,
            cursor=-1
            #total_count=request_limit * 5000
        )

        l.INFO("Getting friends %s" % (kwargs))
        friends = self.api.GetFriendIDs(**kwargs)
        l.INFO("Streaming connections %s friends found" % (len(friends)))
        for friend in friends:
            self.on_connection(user_id, friend, type_=friend)
        return friends

    def _stream_friends_by_screen_name(self, screen_name, request_limit=3):
        kwargs = dict(
            screen_name=screen_name,
            cursor=-1,
            total_count=request_limit * 5000
        )

        l.INFO("Getting friends %s" % (kwargs))
        friends = self.api.GetFriendIDs(**kwargs)
        l.INFO("Streaming connections %s friends found" % (len(friends)))
        for friend in friends:
            self.on_connection(user_id, friend, type_=friend)
        return friends

    def _stream_followers_by_id(self, user_id, request_limit):
        kwargs = dict(
            user_id=user_id,
            cursor=-1,
            total_count=request_limit * 5000
        )

        l.INFO("Getting friends %s" % (kwargs))
        followers = self.api.GetFollowerIDs(**kwargs)
        l.INFO("Streaming connections %s followers found" % (len(followers)))
        for follower in followers:
            self.on_connection(user_id, follower, type_=follower)
        return followers

    def _stream_followers_by_screen_name(self, screen_name):
        user = self._fetch_profiles_by_screen_name(screen_name=screen_name)
        return self._stream_followers_by_id(self, user.id)


class StreamTwitter():
    """Stream twitter"""
    # TODO decide use tweepy/build from scratch/add to python-twitter
