from dataclasses import dataclass
from math import pi

from ncjsam.model.etc import Path
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import type_dyn_num
from ncjsam.model.module.entity import Entity


@dataclass
class OrbitControls(Entity):
    damping_factor: type_dyn_num = 0.05
    enable_damping: type_dyn_bool = False
    enable_pan: type_dyn_bool = True
    enable_rotate: type_dyn_bool = True
    enable_zoom: type_dyn_bool = True
    key_pan_speed: type_dyn_num = 7.0
    max_azimuth_angle: type_dyn_num = float('inf')
    max_distance: type_dyn_num = float('inf')
    max_polar_angle: type_dyn_num = pi
    max_zoom: type_dyn_num = float('inf')
    min_azimuth_angle: type_dyn_num = -float('inf')
    min_distance: type_dyn_num = 0
    min_polar_angle: type_dyn_num = 0
    min_zoom: type_dyn_num = 0
    pan_speed: type_dyn_num = 1
    rotate_speed: type_dyn_num = 1
    zoom_speed: type_dyn_num = 1

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/orbit-controls.js',
        })
        result[0]['properties'].update({
            'damping_factor': render_property(self.damping_factor),
            'enable_damping': render_property(self.enable_damping),
            'enable_pan': render_property(self.enable_pan),
            'enable_rotate': render_property(self.enable_rotate),
            'enable_zoom': render_property(self.enable_zoom),
            'key_pan_speed': render_property(self.key_pan_speed),
            'max_azimuth_angle': render_property(self.max_azimuth_angle),
            'max_distance': render_property(self.max_distance),
            'max_polar_angle': render_property(self.max_polar_angle),
            'max_zoom': render_property(self.max_zoom),
            'min_azimuth_angle': render_property(self.min_azimuth_angle),
            'min_distance': render_property(self.min_distance),
            'min_polar_angle': render_property(self.min_polar_angle),
            'min_zoom': render_property(self.min_zoom),
            'pan_speed': render_property(self.pan_speed),
            'rotate_speed': render_property(self.rotate_speed),
            'zoom_speed': render_property(self.zoom_speed),
        })
        return result
