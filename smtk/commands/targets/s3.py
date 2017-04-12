import json

import click
from luigi.s3 import S3Client, S3Target

import smtk.utils.logger as l
import smtk.commands.targets.errors as errors

from smtk.commands.cli import pass_context


def convert(lines, configuration):
    access_key_id = str(configuration['aws_access_key_id'])
    secret_access_key = str(configuration['aws_secret_access_key'])
    bucket = str(configuration['bucket'])
    cfg_filename = str(configuration.get('output_file', ''))

    s3_client = S3Client(access_key_id,
                         secret_access_key)

    targets = {}

    for line in lines:
        try:
            data = json.loads(line)
        except Exception as e:
            raise Exception(errors.PARSING_ERROR % (line, e))

        if 'type' not in data:
            raise Exception(errors.MISSING_KEY_ERROR % ('type', line))

        data_type = data['type']

        if data_type == 'RECORD':
            if 'stream' not in data:
                raise Exception(errors.MISSING_KEY_ERROR % ('stream', line))

            filename = cfg_filename
            if filename == "":
                filename = data['stream'] + '.json'

            target_path = (
                's3://{bucket}/{filename}'
                .format(bucket=bucket, filename=filename)
            )

            record = data['record']
            print(targets)

            target = None
            if not target_path in targets.keys():
                target = S3Target(target_path, client=s3_client)
                targets[target_path] = {
                    'target': target,
                    'file': target.open('w')
                }

            target = targets[target_path]['target']

            targets[target_path]['file'].write(json.dumps(record) + '\n')

        else:
            l.WARN(errors.UNEXPECTED_MESSAGE_TYPE % (data['type'], data))

    for target_path in targets:
        targets[target_path]['file'].close()


@click.command('s3', short_help="Writes JSON data to s3")
@click.option('--config', required=True)
@pass_context
def cli(ctx, config):
    s3_config = {}

    try:
        with open(config, 'r') as config_file:
            s3_config = json.load(config_file)
            l.INFO("Using custom CSV configuration: %s" % (s3_config))
    except TypeError:
        l.WARN("Unable to parse s3 config")

    input_ = click.get_text_stream('stdin')
    convert(input_, configuration=s3_config)
