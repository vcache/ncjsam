import math
import json

from dataclasses import dataclass
from typing import Union, Optional, NamedTuple

from ncjsam.model.etc import UnJson


# NOTE-A: remove these default Nones, they need only as workaround
#         for python<=3.9 which doesn't support "kw_only"
#         should migrate to python=>3.10 and remove fake Optionals


# Common types and structures


class Expr(NamedTuple):
    expr: str

    def compile(self):
        return {'expr': self.expr}


class Vector2(NamedTuple):
    x: Union[float, int]
    y: Union[float, int]

    @staticmethod
    def deserialize(data):
        return Vector2(x=data[0], y=data[1])

    @staticmethod
    def match(data):
        return type(data) == list

    def compile(self):
        return {'vector2d': [self.x, self.y]}


class Vector3(NamedTuple):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]

    @staticmethod
    def deserialize(data):
        return Vector3(x=data[0], y=data[1], z=data[2])

    @staticmethod
    def match(data):
        return type(data) == list

    def compile(self):
        return {'vector3d': [self.x, self.y, self.z]}


class Vector4(NamedTuple):
    x: Union[float, int]
    y: Union[float, int]
    z: Union[float, int]
    w: Union[float, int]

    @staticmethod
    def deserialize(data):
        return Vector4(x=data[0], y=data[1], z=data[2], w=data[3])

    @staticmethod
    def match(data):
        return type(data) == list

    def compile(self):
        return {'vector4d': [self.x, self.y, self.z, self.w]}


class RgbColor(NamedTuple):
    r: Union[float, int]
    g: Union[float, int]
    b: Union[float, int]

    @staticmethod
    def deserialize(data):
        return RgbColor(r=data[0], g=data[1], b=data[2])

    @staticmethod
    def match(data):
        return type(data) == list

    def compile(self):
        return {'rgb': [self.r, self.g, self.b]}


@dataclass
class Rect:
    left: Union[float, int] = 0
    top: Union[float, int] = 0
    right: Union[float, int] = 0
    bottom: Union[float, int] = 0

    @staticmethod
    def deserialize(data):
        return (UnJson(data).done(Rect))

    @staticmethod
    def match(data):
        return type(data) == dict

    def compile(self):
        return {
            'left': self.left,
            'top': self.top,
            'right': self.right,
            'bottom': self.bottom,
        }


# TODO: infer these types from Voluptios' schemas
type_dyn_expr = Expr
type_dyn_bool = Union[bool, type_dyn_expr]
type_dyn_num = Union[type_dyn_expr, float, int]
type_dyn_str = Union[str, type_dyn_expr]
type_dyn_filename = Union[str, type_dyn_expr]
type_dyn_list = Union[type_dyn_expr, list]
type_dyn_dict = Union[type_dyn_expr, dict]
type_dyn_vector2 = Union[type_dyn_expr, Vector2]
type_dyn_vector3 = Union[type_dyn_expr, Vector3]
type_dyn_rgb = Union[type_dyn_expr, RgbColor]
type_dyn_vector4 = Union[type_dyn_expr, Vector4]
type_dyn_rect = Union[type_dyn_expr, Rect]


@dataclass
class Transformation:
    translate: Optional[type_dyn_vector3] = None
    scale: Optional[type_dyn_vector3] = None
    euler_angles: Optional[type_dyn_vector3] = None
    axis_angle: Optional[type_dyn_vector4] = None
    quaternion: Optional[type_dyn_vector4] = None

    @staticmethod
    def deserialize(data):
        return (
            UnJson(data)
            .replace('translate', Vector3.deserialize, cond=Vector3.match)
            .replace('scale', Vector3.deserialize, cond=Vector3.match)
            .replace('euler-angles', Vector3.deserialize, cond=Vector3.match)
            .replace('axis-angle', Vector4.deserialize, cond=Vector4.match)
            .replace('quaternion', Vector4.deserialize, cond=Vector4.match)
            .done(Transformation))

    def compile(self):
        result = {}
        if self.translate:
            result.update({'translate': render_property(self.translate)})
        if self.euler_angles:
            result.update({'euler_angles': render_property(self.euler_angles)})
        if self.axis_angle:
            result.update({'axis_angle': render_property(self.axis_angle)})
        if self.quaternion:
            result.update({'quaternion': render_property(self.quaternion)})
        if self.scale:
            result.update({'scale': render_property(self.scale)})
        return result


@dataclass
class Texture:
    filename: str

    @staticmethod
    def deserialize(data):
        return Texture(filename=data)

    def compile(self):
        return {
            'filename': self.filename
        }


@dataclass
class Layout:
    x: type_dyn_str
    y: type_dyn_str
    width: type_dyn_str
    height: type_dyn_str
    margin: Optional[type_dyn_rect] = Rect()  # TODO: this is margin actually

    @staticmethod
    def deserialize(data):
        return (
            UnJson(data)
            .replace('margin', Rect.deserialize, cond=Rect.match)
            .done(Layout))

    def compile(self):
        return {
            'x': render_property(self.x),
            'y': render_property(self.y),
            'width': render_property(self.width),
            'height': render_property(self.height),
            'margin': render_property(self.margin)
        }


def render_property(value):
    if bool == type(value):
        return {True: 'true', False: 'false'}[value]
    if value is None:
        return 'null'
    if str == type(value):
        return json.dumps(value)
    if float == type(value):
        if math.isinf(value):
            return f'{"-" if value < 0 else ""}Infinity'
    compile_method = getattr(value, 'compile', None)
    if compile_method:
        return compile_method()
    return value
