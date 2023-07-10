from dataclasses import dataclass
from math import pi

from ncjsam.model.etc import Path
from ncjsam.model.types import RgbColor
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import type_dyn_num
from ncjsam.model.types import type_dyn_rgb
from ncjsam.model.module.entity import Entity


@dataclass
class AmbientLight(Entity):
    color: type_dyn_rgb = None  # TODO: NOTE-A
    intensity: type_dyn_num = 1

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('color', RgbColor.deserialize, cond=RgbColor.match)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/ambient-light.js',
        })
        result[0]['properties'].update({
            'color': render_property(self.color),
            'intensity': render_property(self.intensity),
        })
        return result


@dataclass
class PointLight(Entity):
    color: type_dyn_rgb = None  # TODO: NOTE-A
    intensity: type_dyn_num = 1
    distance: type_dyn_num = 0
    decay: type_dyn_num = 2
    cast_shadow: type_dyn_bool = False

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('color', RgbColor.deserialize, cond=RgbColor.match)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/point-light.js',
        })
        result[0]['properties'].update({
            'color': render_property(self.color),
            'intensity': render_property(self.intensity),
            'distance': render_property(self.distance),
            'decay': render_property(self.decay),
            'cast_shadow': render_property(self.cast_shadow),
        })
        return result


@dataclass
class SpotLight(Entity):
    color: type_dyn_rgb = None  # TODO: NOTE-A
    intensity: type_dyn_num = 1
    distance: type_dyn_num = 0
    decay: type_dyn_num = 2
    cast_shadow: type_dyn_bool = False
    angle: type_dyn_num = pi/2
    penumbra: type_dyn_num = 0

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('color', RgbColor.deserialize, cond=RgbColor.match)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/spot-light.js',
        })
        result[0]['properties'].update({
            'color': render_property(self.color),
            'intensity': render_property(self.intensity),
            'distance': render_property(self.distance),
            'decay': render_property(self.decay),
            'cast_shadow': render_property(self.cast_shadow),
            'angle': render_property(self.angle),
            'penumbra': render_property(self.penumbra),
        })
        return result
