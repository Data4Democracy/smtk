
from smtk.twitter import CollectTwitter
#
twitter = CollectTwitter()
# profile = twitter.get_profiles(screen_names=['bstarling_'], ids=[2496856376])
#
#
# twitter.get_friends(screen_names=['bstarling_'])

# twitter.get_tweets(screen_names=['bstarling_'])

twitter.get_friends(screen_names=['bstarling_'])
twitter.get_followers(screen_names=['bstarling_'])

# from smtk.twitter import CollectTwitter
#
# twitter = CollectTwitter()
# profile = twitter.get_friends(ids=[2496856376])

