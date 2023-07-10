from dataclasses import dataclass, field
from typing import Optional, Dict

from ncjsam.model.module.application import Application
from ncjsam.model.module.entity import Entity, entities_dict_factory
from ncjsam.model.etc import UnJson
from ncjsam.model.etc import Path


@dataclass
class Module:
    ncjsam: str
    package: str
    application: Optional[Application] = None
    entities: Dict[str, Entity] = field(default_factory=dict)

    @staticmethod
    def deserialize(data):
        return (UnJson(data).replace('application', Application.deserialize)
                            .replace('entities', entities_dict_factory)
                            .done(Module))

    def compile(self):
        result = []
        path = Path.parse(self.package)
        for _, entity in self.entities.items():
            result.extend(entity.compile(parent_path=path))
        return result

    def get_assets(self):
        result = []
        for _, entity in self.entities.items():
            result.extend(entity.get_assets())
        return result

    def get_root_ids(self):
        return [
            i.id for _, i in self.entities.items()
        ]
