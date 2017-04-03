from smtk.collect_twitter import CollectTwitter
from smtk.facebook import CollectFacebook
twitter = CollectTwitter()
profile = twitter.get_friends(ids=[2496856376])

# 
# f = CollectFacebook()
# posts = f.get_posts(page_id='5550296508')
#
# for post in posts:
#     print(post)
