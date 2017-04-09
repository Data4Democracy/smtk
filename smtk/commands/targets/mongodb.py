import json

import click

from pymongo import MongoClient

import smtk.utils.logger as l
from smtk.commands.cli import pass_context

# TODO: Read From config file.
# Model mongo data from singer schema
# Upsert instead?

PARSING_ERROR = "Unable to parse:\n%s \nReason: %s"
MISSING_KEY_ERROR = "Line is missing required key '%s':\n%s"

def insert_lines(collection, lines):

    for line in lines:
        try:
            data = json.loads(line)
        except Exception as e:
            raise Exception(PARSING_ERROR%(line, e))

        if 'type' not in data:
            raise Exception(MISSING_KEY_ERROR%('type', line))

        data_type = data['type']

        if data_type == 'RECORD':
            if 'stream' not in data:
                raise Exception(MISSING_KEY_ERROR%('stream', line))

            record = data['record']
            collection.insert_one(record)

        else:
            l.WARN("""
                   Unexpected message type %s in message %s
                   """ %(data['type'], data))


@click.command('mongodb', short_help="Write JSON data to mongodb")
@click.option('--config')
@pass_context
def cli(ctx, config):
    client = MongoClient('rs1deep.local', 27017)
    db = client.twitter_connections
    collection = db.relationships

    input_ = click.get_text_stream('stdin')
    insert_lines(collection, input_)
