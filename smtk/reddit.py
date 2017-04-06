import praw
from smtk.utils import helpers
import logging

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CollectReddit:

    def __init__(self, stream=True):
        self.auth = helpers.reddit_auth()
        self.api = praw.Reddit(**self.auth)
        self.stream = stream

    def on_redditor(self, redditor):
        """Called when redditor (user account) is found"""
        logger.info("{}".format(redditor))

    def on_submission(self, submission):
        """Called when submission is found"""
        pass

    def on_comment(self, comment):
        """Called when a comment is found"""
        logger.info("{}".format(comment))

    def get_redditors(self, names=None, stream=True):
        """Gets redditor profiles by usernames"""

        redditors = self._fetch_redditors_by_name(names=names)
        logger.info("Fetching {} profile(s)".format(len(names)))

        return redditors

    def get_comments(self, ids=None, names=None):
        """Gets comments by id or username but not both"""
        if ids and names:
            # Exception
            return None

        comments = []
        if ids:
            comments = self._fetch_comments_by_id(ids)
            logger.info("Fetching {} comment(s)".format(len(ids)))
        if names:
            comments = self._fetch_comments_by_name(names)
            logger.info("Fetching {} comment(s)".format(len(comments)))

        return comments

    def get_submissions(self, ids=None, urls=None, usernames=None, limit=100):
        """Get a list of submissions by url or id"""
        # todo add get submission by id
        if (ids or urls) and usernames:
            raise ValueError("Must provide list of IDs "
                             "or usernames, but not both")
        id_submissions = []
        url_submissions = []
        if ids:
            id_submissions = [self.api.submission(id=id) for id in ids]
        if urls:
            url_submissions = [self.api.submission(url=url) for url in urls]
        submissions = id_submissions + url_submissions
        return submissions

    def _fetch_redditors_by_name(self, names=None, stream=True):
        """Returns array of praw.models.Redditor"""
        if names:
            redditors = []
            for name in names:
                redditor = self.api.redditor(name)
                redditors.append(redditor)
                if stream:
                    self.on_redditor(redditor)
            return redditors
        return None

    def _fetch_comments_by_id(self, ids=None, stream=True):
        """Returns array of praw.models.Comment"""
        if ids:
            comments = []
            for id_ in ids:
                comment = self.api.comment(id_)
                comments.append(comment)
                if stream:
                    self.on_comment(comment)
            return comments
        return None

    def _fetch_comments_by_name(self, names=None, limit=10, stream=True):
        """Returns array of paw.models.Comment"""
        if names:
            comments = []
            redditors = self._fetch_redditors_by_name(names, stream=False)
            for redditor in redditors:
                redditor_comments = redditor.comments.new(limit=limit)
                for comment in redditor_comments:
                    comments.append(comment)
                    if stream:
                        self.on_comment(comment)
            return comments
        return None
