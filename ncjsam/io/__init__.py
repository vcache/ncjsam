import yaml
import shutil
import logging

from pathlib import Path
from typing import Dict

from ncjsam.constants import NCJSAM_HEADER
from ncjsam.model.module import Module
from ncjsam.model.validator import validate
from ncjsam.model.types import Expr


# Readers


def fetch_sources(prefix: str) -> Dict[Path, Module]:
    def _js_loader(loader, node):
        return Expr(loader.construct_scalar(node))
    yaml.add_constructor('!js', _js_loader)

    root_dir = Path(prefix)
    logging.info(f'scanning directory: "{str(root_dir.absolute())}"')
    return _fetch_sources(root_dir)


def _fetch_sources(root_dir):
    # Check preconditions
    if not root_dir.exists():
        raise ValueError(f'directory not exists: "{root_dir}"')
    if not root_dir.is_dir():
        raise ValueError(f'not a directory: "{root_dir}"')

    # Recursively iterate over directories and collect sources
    result = {}
    for child in root_dir.iterdir():
        abs_path_str = str(child.absolute())
        if child.is_dir():
            # Recustion call
            nested = _fetch_sources(child)
            result.update(nested)
        elif child.is_file():
            # Recursion leaf
            is_yaml = (
                child.name.endswith('.yaml')
                or child.name.endswith('.yml')
            )
            if is_yaml:
                maybe_source = _maybe_parse_source(child)
                if maybe_source:
                    logging.info(f'loaded source "{abs_path_str}"')
                    result.update({
                        child: maybe_source,
                    })
                else:
                    logging.debug(f'skipping "{abs_path_str}": not a ncjsam')
            else:
                logging.debug(f'skipping "{abs_path_str}": not a YAML')
        else:
            logging.debug(f'skipping "{abs_path_str}": not a regular file')
    return result


def _maybe_parse_source(filename: Path):
    # Check preconditions
    if not filename.exists():
        raise ValueError(f'file not exists: "{filename}"')
    if not filename.is_file():
        raise ValueError(f'not a regular file: "{filename}"')

    # Read file and try to parse it
    with filename.open() as f:
        parsed = yaml.load(f, Loader=yaml.Loader)
        if NCJSAM_HEADER in parsed:
            return Module.deserialize(validate(parsed))
    return None


# Writers


def eval_dist_path(prefix, destination):
    destination = Path(destination)
    if not destination.is_absolute():
        destination = Path(prefix) / destination
    return destination


def write_outputs(outputs, prefix, destination):
    # Evaluate destination root directory
    destination = eval_dist_path(prefix, destination)

    # Prepare destination directory
    abs_dst = str(destination.absolute())
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f'destination is not a directory: "{abs_dst}"')
    else:
        logging.info(f'creating directory "{abs_dst}"')
        destination.mkdir(parents=True, exist_ok=True)

    # Perform writing
    for name, data in outputs.items():
        filename = destination / name
        filename_str = str(filename.absolute())
        if type(data) == str:
            logging.info(
                '%swriting file "%s", %d bytes',
                'over-' if filename.exists() else '',
                filename_str,
                len(data),
            )
            filename.write_text(data)
        elif type(data) == dict and 'copy' in data:
            src_stat = data['copy'].stat()
            dst_stat = filename.stat() if filename.exists() else None
            need_update = not dst_stat or src_stat.st_mtime > dst_stat.st_mtime
            if need_update:
                logging.info(
                    '%swriting file "%s" <-- "%s"',
                    'over-' if filename.exists() else '',
                    filename_str,
                    data['copy'],
                )
                shutil.copy(data['copy'], filename)
            else:
                logging.info(
                    'skipping file "%s": up to date',
                    filename_str,
                )
        else:
            raise ValueError(f'unknown data type: {data}')
