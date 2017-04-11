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
        l.INFO("TWEET FOUND: {}".format(tweet.text))

    def on_profile(self, profile):
        """Called when profile is found"""
        l.INFO(profile)

    def on_start(self):
        """Called when collection is started
        Inherit from CollectTwitter class to override to create """
        pass

    def on_connection(self, account, connection, type_):
        """Called when connection is found"""
        l.INFO("{} found {} with {}".format(type_, account, connection))

    def get_friends(self, ids=None, screen_names=None, request_limit=3):
        """In context of twitter friends are accounts the source is following"""
        if ids:
            for id_ in ids:
                self._stream_friends(user_id=id_, request_limit=request_limit)
        if screen_names:
            for screen_name in screen_names:
                self._stream_friends(screen_name=screen_name, request_limit=request_limit)

    def get_followers(self, ids=None, screen_names=None, request_limit=3):
        if ids:
            for id_ in ids:
                self._stream_followers(user_id=id_, request_limit=request_limit)
        if screen_names:
            for screen_name in screen_names:
                self._stream_followers(
                    screen_name=screen_name, request_limit=request_limit)

    def get_profiles(self, ids=None, screen_names=None):
        # TODO Deal with timeouts

        if ids:
            lookup = []
            remain = len(ids)
            for id_ in ids:
                lookup.append(id_)
                if len(lookup) >= 100:
                    # limit 100 profiles per request
                    self._stream_profiles(ids=lookup, by_id=True)
                    remain -= len(lookup)
                    l.INFO("Fetching {lookup} profiles. {remain} remain".format(
                        lookup, remain))
            l.INFO("Fetching remaining %s profile(s)" % (len(lookup)))
            self._stream_profiles(lookup, by_id=True)

        if screen_names:
            lookup = []
            remain = len(screen_names)
            for sn in screen_names:
                lookup.append(sn)
                if len(lookup) >= 100:
                    # limit 100 profiles per request
                    self._stream_profiles(lookup, by_id=False)
                    remain -= len(lookup)
                    l.INFO("Fetching {lookup} profiles. {remain} remain".format(
                        lookup, remain))
            l.INFO("Fetching remaining %s profile(s)" % (len(lookup)))
            self._stream_profiles(lookup, by_id=False)

    def get_tweets(self, ids=None, screen_names=None, limit=3200):
        if ids:
            for id_ in ids:
                l.INFO("Gathering tweets for user ID {}".format(id_))
                self._stream_tweets(id_=id_, limit=limit)
        if screen_names:
            for screen_name in screen_names:
                l.INFO("Gathering tweets for user {}".format(screen_name))
                self._stream_tweets(screen_name=screen_name, limit=limit)

    def _stream_profiles(self, users, by_id=True):
        if len(users) > 100:
            raise RuntimeError(
                "Too many users to fetch, got: %s" % (len(users)))

        if by_id:
            profiles = self.api.UsersLookup(
                user_id=users, include_entities=False)
        else:
            profiles = self.api.UsersLookup(
                screen_name=users, include_entities=False)

        for profile in profiles:
            self.on_profile(profile)

    def _stream_tweets(self, user_id=None, screen_name=None, limit=3200):
        # TODO rework this to use min/max tweets instead of assuming < 200
        # means done
        kwargs = dict(
            count=200
        )
        tweets_gathered = 0

        while True:
            try:
                l.INFO("Fetching 200 tweets %s" % (kwargs))
                tweets = self.api.GetUserTimeline(**kwargs)
                tweets_gathered += len(tweets)

            except Exception as e:
                l.WARN("%s kwargs %s" % (e, kwargs))
                return None

            l.INFO("Streaming tweets")
            for tweet in tweets:
                self.on_tweet(tweet)

            if tweets_gathered >= limit:
                l.INFO("Per user limit hit {} tweets gathered".format(limit))
                break

            if len(tweets) < 200:
                # TODO Fix - Using <200 as proxy for end of user timeline
                l.INFO("Stream ended < 200 tweets")
                break

            tweet_ids = [tweet.id for tweet in tweets]
            if len(tweet_ids) > 0:
                # Next request start at oldest tweet in current request
                l.INFO("Setting max ID: {}".format(min(tweet_ids)))
                kwargs['max_id'] = min(tweet_ids)

    def _stream_friends(self, user_id=None, screen_name=None, request_limit=3):
        kwargs = dict(
            cursor=-1,
            total_count=request_limit * 5000
        )

        if user_id:
            kwargs['user_id'] = user_id
        if screen_name:
            kwargs['screen_name'] = screen_name

            # User ID needed for connection object
            user_id = self._fetch_profile_by_screen_name(screen_name=[screen_name])[0].id

        l.INFO("Getting friends %s" % (kwargs))
        followers = self.api.GetFriendIDs(**kwargs)
        l.INFO("Streaming connections %s friends found" % (len(followers)))
        for follower in followers:
            self.on_connection(user_id, follower, type_='friend')

    def _stream_followers(self, user_id=None, screen_name=None, request_limit=3):
        kwargs = dict(
            cursor=-1,
            total_count=request_limit * 5000
        )
        if user_id:
            kwargs['user_id'] = user_id
        if screen_name:
            kwargs['screen_name'] = screen_name

            # User ID needed for connection object
            user_id = self._fetch_profile_by_screen_name(screen_name=[screen_name])[0].id

        l.INFO("Getting followers %s" % (kwargs))

        followers = self.api.GetFollowerIDs(**kwargs)
        l.INFO("Streaming connections %s followers found" % (len(followers)))
        for follower in followers:
            self.on_connection(user_id, follower, type_='follower')

    def _fetch_profile_by_screen_name(self, screen_name):
        profile = self.api.UsersLookup(screen_name=screen_name, include_entities=False)
        return profile


class StreamTwitter():
    """Stream twitter"""
    # TODO decide use tweepy/build from scratch/add to python-twitter
