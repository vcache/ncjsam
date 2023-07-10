from dataclasses import dataclass, asdict
from typing import Union, Optional

from ncjsam.model.etc import Path
from ncjsam.model.etc import UnJson
from ncjsam.etc.strings import snake_to_camel
from ncjsam.model.types import RgbColor
from ncjsam.model.types import Vector2
from ncjsam.model.types import Texture
from ncjsam.model.types import type_dyn_rgb
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import type_dyn_num
from ncjsam.model.types import type_dyn_str
from ncjsam.model.types import type_dyn_vector2
from ncjsam.model.types import render_property


@dataclass
class _LineCommon:
    color: Optional[type_dyn_rgb] = RgbColor(1, 1, 1)
    fog: Optional[type_dyn_bool] = True
    linewidth: Optional[type_dyn_num] = 1
    linecap: Optional[type_dyn_str] = 'round'
    linejoin: Optional[type_dyn_str] = 'round'
    map: Optional[Texture] = None


@dataclass
class _LineBasicMaterial(_LineCommon):
    def compile(self, parent_path: Path):
        return {
            'properties': _render_dataclass_properties(self),
            'three_class': 'LineBasicMaterial',
        }

    @staticmethod
    def deserialize(data):
        # TODO: move into a base class
        return (UnJson(data).replace('map', Texture.deserialize)
                            .done(_LineBasicMaterial))

    def get_assets(self):
        return _collect_assets_from_dataclass(self)


@dataclass
class _LineDashedMaterial(_LineCommon):
    dash_size: Optional[type_dyn_num] = 3
    gap_size: Optional[type_dyn_num] = 1
    scale: Optional[type_dyn_num] = 1

    def compile(self, parent_path: Path):
        return {
            'properties': _render_dataclass_properties(self),
            'three_class': 'LineDashedMaterial',
        }

    @staticmethod
    def deserialize(data):
        # TODO: move into a base class
        return (UnJson(data).replace('map', Texture.deserialize)
                            .done(_LineDashedMaterial))

    def get_assets(self):
        return _collect_assets_from_dataclass(self)


@dataclass
class _MeshBasicMaterial:
    alpha_map: Optional[Texture] = None
    ao_map: Optional[Texture] = None
    ao_map_intensity: Optional[type_dyn_num] = 1
    color: Optional[type_dyn_rgb] = RgbColor(1, 1, 1)
    combine: Optional[type_dyn_str] = 'multiply'
    env_map: Optional[Texture] = None
    fog: Optional[type_dyn_bool] = True
    light_map: Optional[Texture] = None
    light_map_intensity: Optional[type_dyn_num] = 1
    map: Optional[Texture] = None
    reflectivity: Optional[type_dyn_num] = 1
    refraction_ratio: Optional[type_dyn_num] = 0.98
    specular_map: Optional[Texture] = None
    wireframe: Optional[type_dyn_bool] = False
    wireframe_linecap: Optional[type_dyn_str] = 'round'
    wireframe_linejoin: Optional[type_dyn_str] = 'round'
    wireframe_linewidth: Optional[type_dyn_num] = 1

    def compile(self, parent_path: Path):
        return {
            'properties': _render_dataclass_properties(self),
            'three_class': 'MeshBasicMaterial',
        }

    @staticmethod
    def deserialize(data):
        return (UnJson(data).replace('alpha-map', Texture.deserialize)
                            .replace('ao-map', Texture.deserialize)
                            .replace('env-map', Texture.deserialize)
                            .replace('light-map', Texture.deserialize)
                            .replace('map', Texture.deserialize)
                            .replace('specular-map', Texture.deserialize)
                            .done(_MeshBasicMaterial))

    def get_assets(self):
        return _collect_assets_from_dataclass(self)


@dataclass
class _MeshStandardMaterial:
    alpha_map: Optional[Texture] = None
    ao_map: Optional[Texture] = None
    ao_map_intensity: Optional[type_dyn_num] = 1
    bump_map: Optional[Texture] = None
    bump_scale: Optional[type_dyn_num] = 1
    color: Optional[type_dyn_rgb] = RgbColor(1, 1, 1)
    displacement_map: Optional[Texture] = None
    displacement_scale: Optional[type_dyn_num] = 1
    displacement_bias: Optional[type_dyn_num] = 0
    emissive: Optional[type_dyn_rgb] = RgbColor(0, 0, 0)
    emissive_map: Optional[Texture] = None
    emissive_intensity: Optional[type_dyn_num] = 1
    env_map: Optional[Texture] = None
    env_map_intensity: Optional[type_dyn_num] = 1
    flat_shading: Optional[type_dyn_bool] = False
    fog: Optional[type_dyn_bool] = True
    light_map: Optional[Texture] = None
    light_map_intensity: Optional[type_dyn_num] = 1
    map: Optional[Texture] = None
    metalness: Optional[type_dyn_num] = 0.0
    metalness_map: Optional[Texture] = None
    normal_map: Optional[Texture] = None
    normal_map_type: Optional[type_dyn_str] = 'tangent-space'
    normal_scale: Optional[type_dyn_vector2] = Vector2(1, 1)
    roughness: Optional[type_dyn_num] = 1.0
    roughness_map: Optional[Texture] = None
    wireframe: Optional[type_dyn_bool] = False
    wireframe_linecap: Optional[type_dyn_str] = 'round'
    wireframe_linejoin: Optional[type_dyn_str] = 'round'
    wireframe_linewidth: Optional[type_dyn_num] = 1

    def compile(self, parent_path: Path):
        return {
            'properties': _render_dataclass_properties(self),
            'three_class': 'MeshStandardMaterial',
        }

    @staticmethod
    def deserialize(data):
        return (UnJson(data).replace('alpha-map', Texture.deserialize)
                            .replace('bump-map', Texture.deserialize)
                            .replace('displacement-map', Texture.deserialize)
                            .replace('emissive-map', Texture.deserialize)
                            .replace('env-map', Texture.deserialize)
                            .replace('light-map', Texture.deserialize)
                            .replace('map', Texture.deserialize)
                            .replace('metalness-map', Texture.deserialize)
                            .replace('normal-map', Texture.deserialize)
                            .replace('roughness-map', Texture.deserialize)
                            .done(_MeshStandardMaterial))

    def get_assets(self):
        return _collect_assets_from_dataclass(self)


@dataclass
class Material:
    opacity: Optional[type_dyn_num] = 1.0
    depth_test: Optional[type_dyn_bool] = True
    depth_write: Optional[type_dyn_bool] = True
    alpha_test: Optional[type_dyn_num] = 0
    side: Optional[type_dyn_str] = 'front'
    material: Union[
        _LineBasicMaterial,
        _LineDashedMaterial,
        _MeshBasicMaterial,
        _MeshStandardMaterial,
    ] = None  # NOTE-A

    def compile(self, parent_path: Path):
        assert self.material
        result = self.material.compile(parent_path)
        result['properties'].update(
            _render_dataclass_properties(self, ['material']),
        )
        return result

    @staticmethod
    def deserialize(data):
        return (
            UnJson(data)
            .replace('line-basic', _LineBasicMaterial.deserialize,
                     key_rewrite='material')
            .replace('line-dashed', _LineDashedMaterial.deserialize,
                     key_rewrite='material')
            .replace('mesh-basic', _MeshBasicMaterial.deserialize,
                     key_rewrite='material')
            .replace('mesh-standard', _MeshStandardMaterial.deserialize,
                     key_rewrite='material')
            .done(Material))

    def get_assets(self):
        return self.material.get_assets()

    @staticmethod
    def get_default_material():
        return _MeshStandardMaterial()


def _render_dataclass_properties(dcls, exclude=[]):
    properties = asdict(dcls).keys()
    return {
        snake_to_camel(key): render_property(getattr(dcls, key))
        for key in properties
        if key not in exclude and getattr(dcls, key)
    }


def _collect_assets_from_dataclass(dcls):
    properties = asdict(dcls).keys()
    result = set([
        getattr(dcls, i).filename for i in properties
        if isinstance(getattr(dcls, i), Texture)
    ])
    return list(result)
