from dataclasses import dataclass
from typing import Optional, Dict

from ncjsam.model.etc import UnJson
from ncjsam.model.etc import Path
from ncjsam.model.types import Transformation
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import render_property


# NOTE-A: remove these default Nones, they need only as workaround for
#         python<=3.9 which doesn't support "kw_only"


@dataclass
class Entity:
    id: str
    is_template: bool = False
    public: bool = False
    visible: type_dyn_bool = True
    transformation: Optional[Transformation] = None

    @classmethod
    def unjson(cls, data):
        klass = cls.__name__
        assert klass in data
        return (UnJson(data).inject('id', data[klass])
                            .remove(klass)
                            .replace('transformation',
                                     Transformation.deserialize,
                                     cond=lambda x: type(x) == dict))

    @staticmethod
    def deserialize(data):
        return deserialize_entity(data)

    def compile(self, parent_path: Path):
        path = parent_path.clone()
        path.append(self.id)
        result = {
            'id': self.id,
            'path': path,
            'is_template': self.is_template,
            'public': self.public,
            'class_name': path.mangle(),
            'properties': {  # TODO: dont call 'render_property' at every
                             # derived class but call it at top-level compile
                             # function
                'visible': render_property(self.visible),
            },
        }
        if self.transformation:
            result.update({
                'transformation': self.transformation.compile(),
            })
        return [result]

    def get_assets(self):
        return []


# High-level API


def deserialize_entity(data) -> Entity:
    from ncjsam.model.module.entities import get_registry

    for entity_class in get_registry():
        if entity_class.__name__ in data:
            return entity_class.deserialize(data)
    raise ValueError(
        f'failed to find corresponding entity class '
        f'for the following data: {data}'
    )


def entities_dict_factory(entities_list_data) -> Dict[str, Entity]:
    entities_list = [deserialize_entity(i) for i in entities_list_data]
    return {i.id: i for i in entities_list}
