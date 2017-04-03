from smtk.collect_twitter import CollectTwitter
from smtk.utils.backend import DataStore

import smtk.utils.logger as l

class BaseCollector(CollectTwitter):
    def on_tweet(self, tweet):
        l.INFO(tweet.text.encode('utf-8'))
        # db.send(tweet)

    def on_start(self):
        # setup DB
        pass

    def on_profile(self, profile):
        # db.send(profile)
        print profile

    def on_connection(self):
        # db.send(connection)
        pass

    def explore_network(self, seed_users):
        # TODO
        # Start with seed user(s) and crawl out finding
        # friends/connections/tweets
        pass

class StdioTweetLogger(CollectTwitter):
    def on_tweet(self, tweet):
        l.INFO("TWEET: %s" %(tweet.text.encode('utf-8')))

    def on_start(self):
        pass

    def on_profile(self, profile):
        l.INFO("PROFILE: %s"%(profile))

    def on_connection(self):
        pass

datastore = DataStore()

# create a db
db = datastore.setup(resource="sqlite:///db.sqlite", collection="twitter")
collect = BaseCollector(CollectTwitter)


tweet_logger = StdioTweetLogger()
tweet_logger.get_tweets(screen_names=['POTUS', 'data4democracy'])

