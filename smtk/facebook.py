import facepy
from smtk.utils import helpers
from datetime import datetime


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

    def get_posts(self, db=None, page_id=None, max_posts=None, before=None, after=None):
        """
        :param page_id: the Facebook page id from which posts should be downloaded.
        :param max_posts: the maximum number of posts that should be downloaded. Works backwards in time: the newest X number of posts will be returned.
        :param before: only posts made before this day will be returned.
        :param after: only posts made after this day will be returned.

        Calls `on_post` for each post returned.
        """

        kwargs = {
            'path': '/' + str(page_id) + '/posts',
            'limit': 100,
            'page': True
        }

        if before:
            before = datetime.strptime(before, "%Y-%m-%d")
        if after:
            after = datetime.strptime(after, "%Y-%m-%d")

        if all([before, after]):
            date_range = True
        else:
            date_range = False

        post_data_pages = self.graph.get(**kwargs)

        i = 0
        for post_data in post_data_pages:
            posts_data = post_data['data']

            for post in posts_data:
                i += 1

                if i == max_posts:
                    return i

                post_time = datetime.strptime(post['created_time'], "%Y-%m-%dT%H:%M:%S+%f")
                
                if date_range is True:

                    if post_time < before and post_time > after:
                        # on_post(db, post, page_id)
                        pass
                    else:
                        if post_time < after:
                            return "Gathered all posts after %s and before %s" % (after, before)
                        else:
                            pass

                elif before:
                    if post_time < before:
                        # on_post()
                        pass
                    else:
                        pass

                elif after:
                    if post_time > after:
                        # on_post(self, db, page_id)
                        pass
                    else:
                        return "Gathered all posts after %s" % (after)

                else:
                    # on_post(self, db, page_id)
                    pass

    def get_reactions(self):
        # accept list of post IDs
        # calls on_reaction for each post ID
        # see
        # https://github.com/Data4Democracy/collect-social/blob/master/collect_social/facebook/get_reactions.py
        pass
