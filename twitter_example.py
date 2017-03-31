from smtk.collect_twitter import CollectTwitter
from smtk.utils.backend import DataStore


class BaseCollector(CollectTwitter):
    def on_tweet(self, tweet):
        # db.send(tweet)
        pass

    def on_start(self):
        # setup DB
        pass

    def on_profile(self):
        # db.send(profile)
        pass

    def on_connection(self):
        # db.send(connection)
        pass

    def explore_network(self, seed_users):
        # TODO
        # Start with seed user(s) and crawl out finding
        # friends/connections/tweets
        pass


datastore = DataStore()

# create a db
db = datastore.setup(resource="sqlite:///db.sqlite", collection="twitter")

collect = BaseCollector(CollectTwitter)
collect.explore_network(['expample_user'])
