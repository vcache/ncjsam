import logging

from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

from ncjsam.model.module import Module
from ncjsam.model.module.application import Application


@dataclass
class CompiledModules:
    flatten_classes: List[dict]
    application: Application
    assets: List[str]
    root_ids: List[str]

    def get_root_entities(self):
        return [
            indx for indx, item in enumerate(self.flatten_classes)
            if not item['is_template'] and item['id'] in self.root_ids
        ]


def compile_modules(modules: Dict[Path, Module]) -> CompiledModules:
    return CompiledModules(
        flatten_classes=_flatten_classes(modules),
        application=_get_single_application(modules),
        assets=_query_assets(modules),
        root_ids=_get_root_entities_ids(modules),
    )


def _flatten_classes(modules: Dict[Path, Module]) -> List[Dict]:
    result = []
    for _, module in modules.items():
        result.extend(module.compile())
    return result


def _get_root_entities_ids(modules: Dict[Path, Module]) -> List[str]:
    result = []
    for _, module in modules.items():
        result.extend(module.get_root_ids())
    return result


def _get_single_application(modules: Dict[Path, Module]) -> Application:
    # Filter possible candidates
    single_application = [
        (k, v.application) for k, v in modules.items()
    ]

    # Valid cases
    if not single_application:
        return Application()
    elif len(single_application) == 1:
        logging.info(f'application defined at "{single_application[0][0]}"')
        return single_application[0][1]

    # Something went wrong
    files = ''.join([f'\n - "{i[0]}"' for i in single_application])
    raise ValueError(
        f'modules collection contains several '
        f'application definitions: {files}'
    )


def _query_assets(modules: Dict[Path, Module]) -> List[str]:
    result = []
    for _, module in modules.items():
        result.extend(module.get_assets())
    return sorted(set([i for i in result if type(i) == str]))
