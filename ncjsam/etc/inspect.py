import inspect
import shutil
import pprint
import yaml

from enum import Enum


def to_dict(value):
    T = type(value)
    if T == list:
        return [
            to_dict(i) for i in value
        ]
    elif T == dict:
        return {
            k: to_dict(v)
            for k, v in value.items()
        }
    elif (
        inspect.isclass(T) and
        not inspect.isbuiltin(T) and
        not isinstance(value, Enum) and
        T not in [type(None), bool, int, float, str] and
        hasattr(value, '__dict__')
    ):
        return {
            value.__class__.__name__:
            {
                k: to_dict(v)
                for k, v in value.__dict__.items()
            }
        }
    return value


def dump(value):
    terminal_size = shutil.get_terminal_size()
    pprint.pprint(
        to_dict(value),
        width=terminal_size.columns,
        compact=False,
    )


def dump_yaml(value):
    print(yaml.safe_dump(to_dict(value)))
