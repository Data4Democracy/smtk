from smtk.collect_twitter import CollectTwitter
from smtk.facebook import CollectFacebook
from smtk.reddit import CollectReddit
# twitter = CollectTwitter()
# profile = twitter.get_friends(ids=[2496856376])


f = CollectFacebook()
posts = f.get_posts(page_id='5550296508')
print(posts)

r = CollectReddit()
user = r.get_comments(['D5R'])

p = r.get_comments(['sCZWVhePWiqW'])
