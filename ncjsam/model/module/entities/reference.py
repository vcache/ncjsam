from dataclasses import dataclass

from ncjsam.model.module.entity import Entity
from ncjsam.model.etc import Path


@dataclass
class Reference(Entity):
    target: Path = None  # TODO: NOTE-A

    def deserialize(cls, data):
        return (cls.unjson(data)
                   .replace('target', Path.parse)
                   .done(cls))
