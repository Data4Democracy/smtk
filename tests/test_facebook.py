import pytest
import unittest
import os
from smtk.facebook import CollectFacebook

class TestFacebook(unittest.TestCase):
    def setUp(self):
        FB_APP_ID = os.environ['FB_APP_ID']
        FB_APP_SECRET = os.environ['FB_APP_SECRET']
        self.auth = [FB_APP_ID,FB_APP_SECRET]
        self.facebook = CollectFacebook(auth=self.auth)

    def test_facebook_auth_init(self):
        self.assertEqual(len(self.facebook.auth), 2)
        self.assertTrue(isinstance(self.facebook.auth[0], str))

    def test_facebook_get_posts(self):

        posts = self.facebook.get_posts(page_id = "689907071131476", max_posts = 20)
        assert posts is not None

if __name__ == '__main__':
    unittest.main()