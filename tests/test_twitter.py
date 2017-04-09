import unittest
from smtk.twitter import CollectTwitter


class TestTwitter(unittest.TestCase):
    def setUp(self):
        self.twitter = CollectTwitter()

    def test_twitter_auth_init(self):
        self.assertEqual(len(self.twitter.auth), 4)
        self.assertTrue(isinstance(self.twitter.auth[0], str))
