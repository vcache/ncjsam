import argparse
import logging
from enum import Enum

from ncjsam import constants
from ncjsam.compiler import BuildTargets


class Command(Enum):
    PARSE = 1
    BUILD = 2
    DAEMON = 3


class StringToLevel(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        level = getattr(logging, values.upper(), None)
        setattr(namespace, self.dest, level)


def parse():
    parser = argparse.ArgumentParser(
        prog='ncjsam',
        description='NCJSAM: Never Code JS AnyMore',
        epilog='Report bugs to <https://github.com/vcache/ncjsam/issues>',
    )
    parser.add_argument(
        'command',
        type=str,
        choices=[i.name.lower() for i in Command],
        help='an operation to perform'
    )
    parser.add_argument(
        'prefix',
        type=str,
        help='a path to a directory with NCJSAM yamls to be translated',
    )
    parser.add_argument(
        '--destination',
        type=str,
        default='dist',
        help='an output directory, default is <prefix>/dist',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='don\' output any files, only simulate',
    )
    parser.add_argument(
        '--build-targets',
        nargs='+',
        type=str,
        choices=[i.name.lower() for i in BuildTargets],
        default=[i.name.lower() for i in BuildTargets],
        help='a list of output artifacts to build',
    )
    parser.add_argument(
        '--js-minification',
        action='store_true',
        help='turn on JS minification',
    )
    # TODO: make zip-archive?
    # TODO: upload to itch.io or similar
    # TODO: modes: build release
    parser.add_argument(
        '--log-level',
        default=logging.INFO,
        action=StringToLevel,
        help='logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)'
    )
    parser.add_argument(
        '--bind-ip',
        type=str,
        help='IP address to bind daemon\'s HTTP servers',
        default='127.0.0.1',
    )
    parser.add_argument(
        '--bind-port',
        type=str,
        help='TCP port for HTTP deamon',
        default='8000',
    )
    parser.add_argument(  # TODO: implement via Websocket instead polling
        '--revision-polling-interval',
        type=int,
        help='an interval for polling for a new code revision (from JS side), '
             'milliseconds',
        default='1000'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {constants.NCJSAM_VERSION}'
    )
    return parser.parse_args()
