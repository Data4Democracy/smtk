import facepy
from smtk.utils import helpers

from smtk.utils import helpers


class CollectFacebook():
    """Sets up a facebook collection.

    Inherit from on_comment, on_post, on_profile, on_reaction, on_start
    to handle stream of data returned by a running collection.
    """

    def __init__(self, auth=None):
        # TODO authentication
        self.auth = helpers.facebook_auth(auth=auth)
        self.graph = facepy.GraphAPI(self.auth)

    def on_comment(self):
        """Called when comment is found"""
        pass

    def on_post(self):
        """Called when post is found"""
        pass

    def on_profile(self):
        """Called when profile is found"""
        pass

    def on_reaction(self):
        """Called when reaction is found"""
        pass

    def on_start(self):
        """Called when collection is started

        Inherit from CollectTwitter class to override to create """
        # verify credentials
        pass

    def get_comments(self):
        # accepts list of post IDs
        # calls on_comment for each comment returned
        # param options: max comments per post
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_comments.py
        pass

    def get_posts(self, db=None, page_id=None, max_posts=None, date_range=None):
        """
        :param page_id: the Facebook page id from which posts should be downloaded.
        :param max_posts: the maximum number of posts that should be downloaded. Works backwards in time: the newest X number of posts will be returned.
        :param date_range: accepts a tuple of dates. Only posts published between these dates will be downloaded.

        Calls `on_post` for each post returned.
        """
        kwargs = {
            'path': '/' + str(page_id) + '/posts',
            'limit': max_posts,
            'page': True
        }

        post_data_pages = self.graph.get(**kwargs)

        return post_data_pages

        # for post_data in post_data_pages:
        #     posts_data = post_data['data']

        #     for post in posts_data:
        #         print(post)
        # pass

    def get_reactions(self):
        # accept list of post IDs
        # calls on_reaction for each post ID
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_reactions.py
        pass
