from dataclasses import dataclass

from ncjsam.model.etc import Path
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_num
from ncjsam.model.module.entity import Entity


@dataclass
class GridDebug(Entity):
    size: type_dyn_num = 10
    divisions: type_dyn_num = 10

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/grid-debug.js',
        })
        result[0]['properties'].update({
            'size': render_property(self.size),
            'divisions': render_property(self.divisions),
        })
        return result
