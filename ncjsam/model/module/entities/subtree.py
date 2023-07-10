from dataclasses import dataclass, field
from typing import Dict

from ncjsam.model.etc import Path
from ncjsam.model.module.entity import Entity
from ncjsam.model.module.entity import entities_dict_factory


@dataclass
class Subtree(Entity):
    # TODO: support Reference (or str) instead Entity
    children: Dict[str, Entity] = field(default_factory=dict)

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data)
                   .replace('children', entities_dict_factory)
                   .done(cls))

    def compile(self, parent_path: Path):
        path = parent_path.clone()
        path.append(self.id)  # TODO: this code is duplicated w/ Entity.compile
        result = []
        for _, i in self.children.items():
            result.extend(i.compile(parent_path=path))
        basic_entity = super().compile(parent_path=parent_path)[0]
        basic_entity.update({
            'template_file': 'entities/subtree-entity.js',
            'children': [
                {
                    'id': i['id'],
                    'path': i['path'],
                    'class_name': i['class_name'],
                } for i in result if i['id'] in self.children
            ],
        })
        result.append(basic_entity)
        return result

    def get_assets(self):
        result = []
        for _, child in self.children.items():
            result.extend(child.get_assets())
        return result
