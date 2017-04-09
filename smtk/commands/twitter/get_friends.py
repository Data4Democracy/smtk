import csv

import click
import singer

import smtk.utils.logger as l
from smtk.commands.cli import pass_context
from smtk.twitter import CollectTwitter

class GetFriendsLogger(CollectTwitter):
    @property
    def schema(self):
        return {
            'properties': {
                'account': {'type': 'string'},
                'connection': {'type': 'string'},
                'type_': {'type': 'string'}
            }
        }

    def on_tweet(self, tweet):
        pass

    def on_start(self):
        singer.write_schema('get_friends',
                            self.schema, ['account', 'connection'])

    def on_profile(self, profile):
        print(profile)

    def on_connection(self, account, connection, type_):
        edge = {
            'account': account,
            'connection': connection,
            'type_': type_
        }
        singer.write_records('get_friends', [edge])


@click.command('get_friends', short_help='Outputs Twitter friends for users in `--users`')
@click.option('--users', required=False,
              help="CSV list of user_ids")
@click.option('--from_file', required=False)
@click.option('--from_pipe/--not-from-pipe', default=False)
@pass_context
def cli(ctx, users, from_file, from_pipe):
    collector = GetFriendsLogger()
    screen_names = []

    if not users is None:
        screen_names = users.split(',')

    if not from_file is None:
        reader = csv.reader(from_file)
        for row in reader:
            screen_names.append(row[0])

    if from_pipe:
        try:
            stdin_text = (
                click
                .get_text_stream('stdin')
                .read().strip()
            ).split('\n')
            for line in stdin_text:
                screen_names.append(line)
        except Exception as e:
            raise RuntimeError("Error while reading pipe: %s" %(e))


    l.INFO("Getting user relationship for users: %s" %(screen_names))
    collector.get_friends(screen_names=screen_names)
