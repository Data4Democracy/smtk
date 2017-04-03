import facepy

from smtk.utils import helpers

class CollectFacebook():
    """Sets up a facebook collection.

    Inherit from on_comment, on_post, on_profile, on_reaction, on_start
    to handle stream of data returned by a running collection.
    """

    def __init__(self, *auth):
        # TODO authentication
        self.auth = helpers.facebook_auth()
        self.graph = facepy.GraphAPI(*self.auth)

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

    def get_posts(self):
        # accepts list of page IDs
        # calls on_post for each post returned
        # param options: max post IDs to return
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_posts.py
        pass

    def get_reactions(self):
        # accept list of post IDs
        # calls on_reaction for each post ID
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_reactions.py
        pass
