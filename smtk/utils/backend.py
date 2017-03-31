import dataset


class DataStore():

    def setup(self, **kwargs):
        backend = kwargs['resource'].split(':')[0]
        if backend == 'sqlite':
            db = setup_sqlite(kwargs['resource'], kwargs['collection'])
            return db


def setup_sqlite(db_url, collection):
    """
    create required tables & indexes
    """
    if collection == 'twitter':
        db = dataset.connect(db_url)

        connections = db['connection']
        users = db['user']
        tweets = db['tweet']
        medias = db['media']
        mentions = db['mention']
        urls = db['url']
        hashtags = db['hashtag']

        tweets.create_index(['tweet_id'])
        medias.create_index(['tweet_id'])
        mentions.create_index(['user_id'])
        mentions.create_index(['mentioned_user_id'])
        urls.create_index(['tweet_id'])
        hashtags.create_index(['tweet_id'])
        users.create_index(['user_id'])
        connections.create_index(['friend_id'])
        connections.create_index(['follower_id'])

    return db
