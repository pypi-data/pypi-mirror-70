#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The CLI module contains all the logic needed to run a CLI."""
import sys
import argparse
import warnings
from os import getenv, path
from json import loads
from jsonschema import validate
from pacifica.uploader.metadata import metadata_decode
from ._version import __version__
from .methods import upload, configure, download
from .utils import system_config_path, user_config_path, compressor_generator


def arg_to_compressor_obj(str_obj=None):
    """Check the argument for either 'bzip2', 'gzip', or None."""
    if str_obj not in [None, 'bzip2', 'gzip']:
        raise argparse.ArgumentTypeError(
            'Value must be "bzip2" or "gzip".'
        )
    return compressor_generator(str_obj)


def mangle_config_argument(argv, default_config):
    """Get the config argument out of argv and return stripped version."""
    config_arg = '--config'
    len_arg = len(config_arg)
    starts_argv = [arg[:len_arg] for arg in argv]
    if config_arg not in starts_argv:
        return (default_config, argv)
    if config_arg in argv:
        config_file = argv[argv.index(config_arg) + 1]
        del argv[argv.index(config_arg) + 1]
        del argv[argv.index(config_arg)]
    else:
        config_file = argv[starts_argv.index(config_arg)][len_arg + 1:]
        del argv[starts_argv.index(config_arg)]
    return (config_file, argv)


def parse_uploader_config(upload_parser, argv):
    """Find the uploader metadata config and parse arguments out of it."""
    upload_file_name = 'uploader.json'
    default_config = getenv(
        'UPLOADER_CONFIG', system_config_path(upload_file_name))
    if default_config == upload_file_name and path.isfile(user_config_path(upload_file_name)):
        default_config = user_config_path(upload_file_name)
    config_file, argv = mangle_config_argument(argv, default_config)
    if not path.isfile(config_file):
        warnings.warn('Config File {} is not a file or is not accessible'.format(config_file))
        return default_config, argv, None
    json_str = open(config_file).read()
    schema = loads(open(path.join(path.dirname(__file__), 'config_schema.json')).read())
    validate(loads(json_str), schema)
    config_data = metadata_decode(json_str)
    for config_part in config_data:
        if not config_part.value:
            upload_parser.add_argument(
                '--{}-regex'.format(config_part.metaID), required=False,
                dest='{}_regex'.format(config_part.metaID),
                help='{} regular expression match.'.format(
                    config_part.displayTitle)
            )
            upload_parser.add_argument(
                '--{}'.format(config_part.metaID), '-{}'.format(
                    config_part.metaID[0]),
                help=config_part.displayTitle, required=False
            )
    return config_file, argv, config_data


def main(argv=None):
    """Main method to deal with command line argument parsing."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    upload_parser = subparsers.add_parser(
        'upload', help='upload help', description='perform upload')
    config_parser = subparsers.add_parser(
        'configure', help='configure help', description='setup configuration')
    download_parser = subparsers.add_parser(
        'download', help='download help', description='perform download')
    if argv is None:
        argv = sys.argv
    default_config, argv, config_data = parse_uploader_config(upload_parser, argv)
    parser.add_argument(
        '--config', dest='config', default=default_config,
        help='Upload configuration metadata.', required=False
    )
    parser.add_argument(
        '--config-ini', dest='config_ini', default=getenv('PACIFICA_CLI_INI', 'config.ini'),
        help='Endpoint configuration ini file.', required=False
    )
    parser.add_argument(
        '--verbose', dest='verbose', default='info',
        help='Enable verbose logging.', required=False
    )
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s {version}'.format(version=__version__)
    )
    upload_parser.add_argument(
        '--follow-links', default=False, action='store_true', dest='followlinks',
        help='Follow links to directories when bundling.', required=False
    )
    upload_parser.add_argument(
        '--nowait', default=True, action='store_false', dest='wait',
        help='Wait for the upload is accepted.', required=False
    )
    upload_parser.add_argument(
        '--local-retry', dest='localretry',
        help='Retry and upload from an existing bundle.', required=False
    )
    upload_parser.add_argument(
        '--local-compress', dest='localcompress', metavar='TYPE',
        help='Compress the local saved file with TYPE of bzip2 or gzip.', required=False,
        type=arg_to_compressor_obj, default=arg_to_compressor_obj()
    )
    upload_parser.add_argument(
        '--local-save', dest='localsave', metavar='FILE',
        help='Save the upload bundle to FILE.', required=False
    )
    upload_parser.add_argument(
        '--tar-in-tar', default=False, action='store_true', dest='tarintar',
        help='Create a tar before we upload.', required=False
    )
    upload_parser.add_argument(
        '--dry-run', default=False, action='store_true', dest='dry_run',
        help='Don\'t upload, stop after query engine.', required=False
    )
    upload_parser.add_argument(
        '--do-not-upload', default=False, action='store_true', dest='do_not_upload',
        help='Don\'t upload, works well with local save option.', required=False
    )
    upload_parser.add_argument(
        '--interactive', default=False, action='store_true', dest='interactive',
        help='Interact with the query engine.', required=False
    )
    upload_parser.add_argument(
        'files', metavar='FILES', nargs='*', help='files you want to upload.'
    )
    download_parser.add_argument(
        '--destination', metavar='DIR', default='.',
        help='download the files to DIR')
    dl_group = download_parser.add_mutually_exclusive_group()
    dl_group.add_argument(
        '--transaction-id', metavar='TRANSID',
        dest='trans_id', default=None,
        help='download the files associated with TRANSID')
    dl_group.add_argument(
        '--cloudevent', metavar='CLOUDEVENT', default=None,
        type=argparse.FileType('r'), dest='cloudevent',
        help='download the files from the cloudevent file.')
    upload_parser.set_defaults(func=upload)
    config_parser.set_defaults(func=configure)
    download_parser.set_defaults(func=download)

    args = parser.parse_args(argv[1:])
    return args.func(args, config_data)


if __name__ == '__main__':
    main()
