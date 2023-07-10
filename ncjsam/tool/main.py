import logging

from termcolor import colored
from ncjsam.daemon import LiveServer
from ncjsam.tool import arguments
from ncjsam.tool.builder import run_build
from ncjsam.io import fetch_sources
from ncjsam.etc import inspect


def _parse_command(args):
    sources = fetch_sources(args.prefix)
    if args.dry_run:
        inspect.dump(sources)


def _build_command(args):
    run_build(args)


def _daemon_command(args):
    logging.info('creating a daemon')
    live_server = LiveServer(args)

    logging.info('building fresh prefix')
    run_build(args, daemon_context=live_server.get_daemon_context())

    logging.info('daemon is about to start')
    live_server.run()


COMMANDS = {
    arguments.Command.PARSE: _parse_command,
    arguments.Command.BUILD: _build_command,
    arguments.Command.DAEMON: _daemon_command,
}


def run():
    args = arguments.parse()
    logging.basicConfig(
        level=args.log_level,
        format=(
            colored('%(asctime)s ', 'blue') +
            colored('%(levelname)s ', 'yellow') +
            colored('%(message)s', 'green')
        ),
    )
    logging.debug(f'arguments are: {args}')
    command = arguments.Command[args.command.upper()]
    COMMANDS[command](args)
