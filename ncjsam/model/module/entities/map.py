from dataclasses import dataclass

from ncjsam.model.module.entity import Entity
from ncjsam.model.module.entity import deserialize_entity
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import type_dyn_dict
from ncjsam.model.etc import Path


# TODO: update by event or timer, by value change (by edge)
@dataclass
class Map(Entity):
    data: type_dyn_dict = None  # TODO: NOTE-A + support int and maybe a list
    update: type_dyn_bool = True  # TODO: expunge it after Expr dependencies
    variable: str = None  # TODO: NOTE-A
    element: Entity = None  # TODO: NOTE-A # TODO: support Reference (or str)

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data)
                   .replace('element', deserialize_entity)
                   .done(cls))

    def compile(self, parent_path: Path):
        path = parent_path.clone()
        path.append(self.id)  # TODO: this code is duplicated w/ Entity.compile
        result = self.element.compile(parent_path=path)
        basic_entity = super().compile(parent_path=parent_path)[0]
        basic_entity.update({
            'template_file': 'entities/map-entity.js',
            'variable': self.variable,  # NOTE: could be accessed from JS
                                        # with 'this.{{ variable }}'
            'element': {
                'id': result[-1]['id'],
                'path': result[-1]['path'],
                'class_name': result[-1]['class_name'],
            },
        })
        basic_entity['properties'].update({
            'data': render_property(self.data),
            'update': render_property(self.update),
        })
        result.append(basic_entity)
        return result

    def get_assets(self):
        return self.element.get_assets()
