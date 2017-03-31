from smtk.collect_twitter import CollectTwitter

twitter = CollectTwitter()
profile = twitter.get_friends(ids=[2496856376])
