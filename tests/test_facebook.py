import pytest
import unittest
import os
from smtk.facebook import CollectFacebook
import datetime

class TestFacebook(unittest.TestCase):
    def setUp(self):
        FB_APP_ID = os.environ['FB_APP_ID']
        FB_APP_SECRET = os.environ['FB_APP_SECRET']
        self.auth = [FB_APP_ID,FB_APP_SECRET]
        self.facebook = CollectFacebook(auth=self.auth)
        self.before = datetime.datetime.today().strftime("%Y-%m-%d")
        after = datetime.datetime.today() - datetime.timedelta(days=2)
        self.after = after.strftime("%Y-%m-%d")


    def test_facebook_auth_init(self):
        self.assertEqual(len(self.facebook.auth), 2)
        self.assertTrue(isinstance(self.facebook.auth[0], str))

    def test_facebook_get_posts(self):

        posts = self.facebook.get_posts(page_id = "689907071131476", max_posts = 20)
        assert posts is not None

    def test_facebook_get_posts_max(self):
        posts = self.facebook.get_posts(page_id = "689907071131476", max_posts = 20)
        self.assertEqual(posts, 20)

    def test_facebook_get_posts_after(self):
        posts = self.facebook.get_posts(page_id = "689907071131476", after=self.after)
        self.assertEqual(posts, "Gathered all posts after %s 00:00:00" % (self.after))

    def test_facebook_get_posts_date_range(self):
        posts = self.facebook.get_posts(page_id = "689907071131476", before=self.before, after=self.after)
        self.assertEqual(posts, "Gathered all posts after %s 00:00:00 and before %s 00:00:00" % (self.after, self.before))

if __name__ == '__main__':
    unittest.main()