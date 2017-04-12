from __future__ import absolute_import

import os
import csv
import json
import click

import smtk.utils.logger as l
import smtk.commands.targets.errors as errors

from smtk.utils.csv import flatten
from smtk.commands.cli import pass_context


CSV_DEFAULT_CONFIG = {
    'output_file': "",
    'delimiter': ',',
    'quotechar': '"'
}


def is_file_empty(filename):
    return (
        (not os.path.isfile(filename)) or
        os.stat(filename).st_size == 0
    )


def convert(lines, configuration):
    cfg_filename = str(configuration.get('output_file', ""))
    delimiter = str(configuration.get('delimiter', ','))
    quotechar = str(configuration.get('quotechar', '"'))

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
                filename = data['stream'] + '.csv'
            flattened_record = flatten(data['record'])
            header = flattened_record.keys()

            with open(filename, 'a') as output_file:
                writer = csv.DictWriter(output_file,
                                        header,
                                        extrasaction='ignore',
                                        delimiter=delimiter,
                                        quotechar=quotechar)

                if is_file_empty(filename):
                    writer.writeheader()
                writer.writerow(flattened_record)

        else:
            l.WARN(errors.UNEXPECTED_MESSAGE_TYPE % (data['type'], data))


@click.command('csv', short_help="Writes JSON data to CSV")
@click.option('--config')
@pass_context
def cli(ctx, config):
    csv_config = {}

    try:
        with open(config, 'r') as config_file:
            csv_config = json.load(config_file)
            l.INFO("Using custom CSV configuration: %s" % (csv_config))
    except TypeError:
        l.WARN("Using default CSV configuration: %s" % (CSV_DEFAULT_CONFIG))

    input_ = click.get_text_stream('stdin')
    convert(input_, configuration=csv_config)
