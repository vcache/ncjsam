from dataclasses import dataclass
from typing import Optional

from ncjsam.model.etc import Path
from ncjsam.model.types import Vector3
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_num
from ncjsam.model.types import type_dyn_vector3
from ncjsam.model.module.entity import Entity


@dataclass
class PerspectiveCamera(Entity):
    fov: type_dyn_num = 50
    near: type_dyn_num = 0.1
    far: type_dyn_num = 2000
    look_at: Optional[type_dyn_vector3] = None

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('look-at', Vector3.deserialize, cond=Vector3.match)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/perspective-camera.js',
        })
        result[0]['properties'].update({
            'fov': render_property(self.fov),
            'near': render_property(self.near),
            'far': render_property(self.far),
            'look_at': render_property(self.look_at),
        })
        return result
