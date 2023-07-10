from dataclasses import dataclass

from typing import List, Optional

from ncjsam.model.etc import Path
from ncjsam.model.module.entity import Entity
from ncjsam.model.module.entities.view.materials import Material

from ncjsam.model.types import Vector2
from ncjsam.model.types import Vector3
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_num
from ncjsam.model.types import type_dyn_str
from ncjsam.model.types import type_dyn_vector2
from ncjsam.model.types import type_dyn_vector3


@dataclass
class PlaneView(Entity):
    dimensions: type_dyn_vector2 = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('dimensions', Vector2.deserialize, cond=Vector2.match)
            .replace('material', Material.deserialize)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/plane-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'dimensions': render_property(self.dimensions),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class BoxView(Entity):
    dimensions: type_dyn_vector3 = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (
            cls.unjson(data)
            .replace('dimensions', Vector3.deserialize, cond=Vector3.match)
            .replace('material', Material.deserialize)
            .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/box-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'dimensions': render_property(self.dimensions),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class SphereView(Entity):
    radius: type_dyn_num = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('material', Material.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/sphere-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'radius': render_property(self.radius),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class CapsuleView(Entity):
    radius: type_dyn_num = None  # TODO: NOTE-A
    length: type_dyn_num = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('material', Material.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/capsule-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'radius': render_property(self.radius),
            'length': render_property(self.length),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class CylinderView(Entity):
    top_radius: type_dyn_num = None  # TODO: NOTE-A
    bottom_radius: type_dyn_num = None  # TODO: NOTE-A
    height: type_dyn_num = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('material', Material.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/cylinder-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'top_radius': render_property(self.top_radius),
            'bottom_radius': render_property(self.bottom_radius),
            'height': render_property(self.height),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class ConeView(Entity):
    radius: type_dyn_num = None  # TODO: NOTE-A
    height: type_dyn_num = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('material', Material.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/cone-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'radius': render_property(self.radius),
            'height': render_property(self.height),
        })
        return result

    def get_assets(self):
        return self.material.get_assets() if self.material else []


@dataclass
class MeshView(Entity):
    filename: type_dyn_str = None               # TODO: NOTE-A
    preload_assets: Optional[List[str]] = None  # TODO: NOTE-A
    material: Optional[Material] = Material.get_default_material()
    animation: Optional[type_dyn_str] = None

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('material', Material.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/mesh-view.js',
        })
        if self.material:
            result[0].update({'material': self.material.compile(parent_path)})
        result[0]['properties'].update({
            'filename': render_property(self.filename),
            'animation': render_property(self.animation),
        })
        return result

    def get_assets(self):
        result = (
            set([self.filename]) |
            set(self.preload_assets or []) |
            set(self.material.get_assets() if self.material else [])
        )
        return list(result)
