import sys


def perform_test():
    try:
        import termcolor  # noqa
        import jinja2  # noqa
        import jsmin  # noqa
        import yaml  # noqa
        import voluptuous  # noqa
        import pygments  # noqa
        import aiohttp  # noqa
        import asyncinotify  # noqa
    except ModuleNotFoundError as e:
        print(e)
        print('Please install requirements:')
        print('  pip3 install -r requirements.txt')
        sys.exit(1)
