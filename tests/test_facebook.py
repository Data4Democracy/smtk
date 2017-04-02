import pytest
import unittest
from smtk.facebook import CollectFacebook
from smtk.utils.api_keys import FB_APP_ID, FB_APP_SECRET, FB_API_VERSION

class TestFacebook(unittest.TestCase):
    def setUp(self):
        self.auth = [FB_APP_ID,FB_APP_SECRET,'2.8']
        self.facebook = CollectFacebook(*self.auth)

    def test_facebook_auth_init(self):
        self.assertEqual(len(self.facebook.auth), 2)
        self.assertTrue(isinstance(self.facebook.auth[0], str))
        self.assertEqual(self.facebook.auth[1],FB_API_VERSION)

    def test_facebook_get_posts(self):

        posts = self.facebook.get_posts(page_id = "689907071131476", max_posts = 20)
        assert posts is not None

if __name__ == '__main__':
    unittest.main()