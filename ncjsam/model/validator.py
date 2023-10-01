import re

from voluptuous import Optional, Required, Schema, Any, All, Self, Exclusive, \
                       Length, In
from voluptuous.error import Invalid

from ncjsam.model.types import Expr


# Custom validators


def _validate_ncjsam(data):
    if not re.match('^[0-9]+\\.[0-9]+$', data):
        raise Invalid(f'ncjsam version format is invalid: "{data}"')
    return data


def _validate_package(data):
    if not re.match('^[a-zA-Z_][a-zA-Z0-9_\\.-]*$', data):
        raise Invalid(f'package format is invalid: "{data}"')
    return data


def _validate_id(data):
    return _validate_package(data)


def _validate_path(data):
    if not re.match('^(\\/[a-zA-Z_][a-zA-Z0-9_\\.-]*)+\\/?$', data):
        raise Invalid(f'path format is invalid: "{data}"')
    return data


def _percentage(data):
    if type(data) != str:
        raise Invalid('not a string')
    if not re.match('^([0-9]+|\\.[0-9]+|[0-9]+.[0-9]*)\\w*%$', data):
        raise Invalid(f'ncjsam percentage format is invalid: "{data}"')
    return data


def _pixelage(data):
    if type(data) != str:
        raise Invalid('not a string')
    if not re.match('^([0-9]+|\\.[0-9]+|[0-9]+.[0-9]*)\\w*px$', data):
        raise Invalid(f'ncjsam pixelage format is invalid: "{data}"')
    return data


def _gui_size_modes(data):
    FILTER = ('auto')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected gui size mode: "{data}", '
                      f'allowed values are {FILTER}')
    return data


def _always_true(data):
    return data


def _side(data):
    FILTER = ('front', 'back', 'double')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected material side constant: "{data}", '
                      f'allowed values are {FILTER}')
    return data


def _linecap(data):
    FILTER = ('butt', 'round', 'square')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected material line cap constant: "{data}", '
                      f'allowed values are {FILTER}')
    return data


def _linejoin(data):
    FILTER = ('round', 'bevel', 'miter')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected material line join constant: "{data}", '
                      f'allowed values are {FILTER}')
    return data


def _combine(data):
    FILTER = ('multiply', 'mix', 'add')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected material combine constant: "{data}", '
                      f'allowed values are {FILTER}')
    return data


def _normal_map_type(data):
    FILTER = ('tangent', 'object')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected material normal map type constant: '
                      f'"{data}", allowed values are {FILTER}')
    return data


def _sprite_mode(data):
    FILTER = ('2d', '3d', '3d-faced')
    if not (data.lower() in FILTER):
        raise Invalid(f'unexpected sprite mode type constant: "{data}", '
                      f'allowed values are {FILTER}')
    return data


# Schemas


_application_schema = Schema({
    Optional('meta-info'): {
        Optional('authors'): [str],
        Optional('version'): str,
        Optional('title'): str,
        Optional('description'): str,
    },
    Optional('render'): {
        Optional('debug-physics'): bool,
    },
    Optional('window'): {
        Optional('title'): str,
        Optional('mode'): In({'fullscreen', 'windowed'}),
        Optional('resizable'): bool,
    },
})


_const_vec2 = All([float, int], Length(2, 2))
_const_vec3 = All([float, int], Length(3, 3))
_const_vec4 = All([float, int], Length(4, 4))
_const_rect = {
    Optional('left'): Any(float, int),
    Optional('top'): Any(float, int),
    Optional('right'): Any(float, int),
    Optional('bottom'): Any(float, int),
}


# TODO: map these types from the model.types.* and model.module.entities.*
_dyn_expr = Expr
_dyn_bool = Any(bool, _dyn_expr)
_dyn_num = Any(_dyn_expr, float, int)
_dyn_str = Any(str, _dyn_expr)
_dyn_filename = Any(str, _dyn_expr)
_dyn_list = Any(_dyn_expr, list)
_dyn_tree_path = All(str, _validate_path)
_dyn_vector2 = Any(_dyn_expr, _const_vec2)
_dyn_vector3 = Any(_dyn_expr, _const_vec3)
_dyn_rgb = Any(_dyn_expr, _const_vec3)
_dyn_vector4 = Any(_dyn_expr, _const_vec4)
_dyn_transformation = {
    Optional('translate'): _dyn_vector3,
    Optional('scale'): _dyn_vector3,
    Exclusive('euler-angles', 'rotation'): _dyn_vector3,
    Exclusive('axis-angle', 'rotation'): _dyn_vector4,
    Exclusive('quaternion', 'rotation'): _dyn_vector4,
}
_dyn_rect = Any(_dyn_expr, _const_rect)
_dyn_layout = Any(_pixelage, _percentage, Expr)


_dyn_linecap = Any(Expr, _linecap)
_dyn_linejoin = Any(Expr, _linejoin)
_dyn_combine = Any(Expr, _combine)
_dyn_normal_map_type = Any(Expr, _normal_map_type)
_dyn_material_line_basic_material = {
    Optional('color'): _dyn_rgb,
    Optional('fog'): _dyn_bool,
    Optional('linewidth'): _dyn_num,
    Optional('linecap'): _dyn_linecap,
    Optional('linejoin'): _dyn_linejoin,
    Optional('map'): str,  # TODO _dyn_filename,
}
_dyn_material = {
    # Common properties
    Optional('opacity'): _dyn_num,  # when omitted => "not transparent"
    Optional('depth-test'): _dyn_bool,
    Optional('depth-write'): _dyn_bool,
    Optional('alpha-test'): _dyn_num,
    Optional('side'): Any(_dyn_expr, _side),

    # TODO: implement dynamic change of material
    Exclusive('line-basic', 'material'): {  # LineBasicMaterial
        **_dyn_material_line_basic_material
    },
    Exclusive('line-dashed', 'material'): {  # LineDashedMaterial
        Optional('dash-size'): _dyn_num,
        Optional('gap-size'): _dyn_num,
        Optional('scale'): _dyn_num,
        **_dyn_material_line_basic_material,
    },
    Exclusive('mesh-basic', 'material'): {  # MeshBasicMaterial
        Optional('alpha-map'): str,  # TODO _dyn_filename,
        Optional('ao-map'): str,  # TODO _dyn_filename,
        Optional('ao-map-intensity'): _dyn_num,
        Optional('color'): _dyn_rgb,
        Optional('combine'): _dyn_combine,
        Optional('env-map'): str,  # TODO _dyn_filename,
        Optional('fog'): _dyn_bool,
        Optional('light-map'): str,  # TODO _dyn_filename,
        Optional('light-map-intensity'): _dyn_num,
        Optional('map'): str,  # TODO _dyn_filename,
        Optional('reflectivity'): _dyn_num,
        Optional('refraction-ratio'): _dyn_num,
        Optional('specular-map'): str,  # TODO _dyn_filename,
        Optional('wireframe'): _dyn_bool,
        Optional('wireframe-linecap'): _dyn_linecap,
        Optional('wireframe-linejoin'): _dyn_linejoin,
        Optional('wireframe-linewidth'): _dyn_num,
    },
    Exclusive('mesh-standard', 'material'): {  # MeshStandardMaterial
        Optional('alpha-map'): str,  # TODO _dyn_filename,
        Optional('ao-map'): str,  # TODO _dyn_filename,
        Optional('ao-map-intensity'): _dyn_num,
        Optional('bump-map'): str,  # TODO _dyn_filename,
        Optional('bump-scale'): _dyn_num,
        Optional('color'): _dyn_rgb,
        Optional('displacement-map'): str,  # TODO _dyn_filename,
        Optional('displacement-scale'): _dyn_num,
        Optional('displacement-bias'): _dyn_num,
        Optional('emissive'): _dyn_rgb,
        Optional('emissive-map'): str,  # TODO _dyn_filename,
        Optional('emissive-intensity'): _dyn_num,
        Optional('env-map'): str,  # TODO _dyn_filename,
        Optional('env-map-intensity'): _dyn_num,
        Optional('flat-shading'): _dyn_bool,
        Optional('fog'): _dyn_bool,
        Optional('light-map'): str,  # TODO _dyn_filename,
        Optional('light-map-intensity'): _dyn_num,
        Optional('map'): str,  # TODO _dyn_filename,
        Optional('metalness'): _dyn_num,
        Optional('metalness-map'): str,  # TODO _dyn_filename,
        Optional('normal-map'): str,  # TODO _dyn_filename,
        Optional('normal-map-type'): _dyn_normal_map_type,
        Optional('normal-scale'): _dyn_vector2,
        Optional('roughness'): _dyn_num,
        Optional('roughness-map'): str,  # TODO _dyn_filename,
        Optional('wireframe'): _dyn_bool,
        Optional('wireframe-linecap'): _dyn_linecap,
        Optional('wireframe-linejoin'): _dyn_linejoin,
        Optional('wireframe-linewidth'): _dyn_num,
    },
    # TODO: add other materials
}


def _make_common_node(klass, remainder):
    return {
        Required(klass): All(str, _validate_id),  # TODO: allow aliases in list
        Optional('is-template'): bool,
        Optional('public'): bool,
        Optional('visible'): _dyn_bool,
        Optional('transformation'): _dyn_transformation,
        **remainder,
    }


def _make_gui_node(klass, remainder):
    return {
        Required(klass): All(str, _validate_id),  # TODO: allow aliases in list
        Required('layout'): {
            # NOTE: 'percentage' is always a share of a container
            Required('x'): _dyn_layout,  # 0%: left; 50%: center; 100%: right
            Required('y'): _dyn_layout,  # 0%: top; 50%: center; 100%: bottom
            Required('width'): Any(_dyn_layout, _gui_size_modes),
            Required('height'): Any(_dyn_layout, _gui_size_modes),
            Optional('margin'): _dyn_rect,
        },
        Optional('is-template'): bool,
        Optional('public'): bool,
        Optional('visible'): _dyn_bool,
        Optional('catch-input'): _dyn_bool,
        **remainder,
    }


_entity_schema = Schema(Any(
    # Tree structural elements
    _make_common_node('Subtree', {
        Required('children'): [Self],
    }),
    _make_common_node('Map', {
        Required('data'): Any(Expr, int, dict),
        Optional('update'): Any(Expr, bool),
        Required('variable'): str,
        Required('element'): Any(str, Self),
    }),
    _make_common_node('Reference', {
        Required('target'): _dyn_tree_path,
    }),

    # Properties
    _make_common_node('Variable', {
        Required('default-value'): _always_true,  # TODO: Any(_json, _dyn_expr)
    }),
    _make_common_node('Constant', {
        Required('default-value'): _always_true,  # TODO: Any(_json, _dyn_expr)
    }),
    _make_common_node('Function', {
        Required('expression'): _dyn_expr,
    }),

    # Triggers
    _make_common_node('Trigger', {
        Required('events'): [str],
        Required('action'): _dyn_expr,
        Optional('condition'): _dyn_bool,
    }),

    # Lights
    _make_common_node('AmbientLight', {
        Required('color'): _dyn_rgb,
        Optional('intensity'): _dyn_num,
    }),
    _make_common_node('PointLight', {
        Required('color'): _dyn_rgb,
        Optional('cast-shadow'): _dyn_bool,
        Optional('decay'): _dyn_num,
        Optional('intensity'): _dyn_num,
        Optional('distance'): _dyn_num,
    }),
    _make_common_node('SpotLight', {
        Required('color'): _dyn_rgb,
        Optional('cast-shadow'): _dyn_bool,
        Optional('decay'): _dyn_num,
        Optional('intensity'): _dyn_num,
        Optional('distance'): _dyn_num,
        Optional('angle'): _dyn_num,
        Optional('penumbra'): _dyn_num,
        Optional('target'): _dyn_expr,
    }),

    # Views
    _make_common_node('PlaneView', {
        Required('dimensions'): _dyn_vector2,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('BoxView', {
        Required('dimensions'): _dyn_vector3,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('SphereView', {
        Required('radius'): _dyn_num,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('CapsuleView', {
        Required('radius'): _dyn_num,
        Required('length'): _dyn_num,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('CylinderView', {
        Required('top-radius'): _dyn_num,
        Required('bottom-radius'): _dyn_num,
        Required('height'): _dyn_num,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('ConeView', {
        Required('radius'): _dyn_num,
        Required('height'): _dyn_num,
        Optional('material'): _dyn_material,
    }),
    _make_common_node('MeshView', {
        Required('filename'): _dyn_filename,
        # TODO: this is hack, make to infere list of assets automatically
        Optional('preload-assets'): [str],
        Optional('material'): _dyn_material,
        Optional('animation'): _dyn_str,
    }),

    # Sprites
    _make_common_node('TextSprite', {
        Required('mode'): _sprite_mode,
        Required('text'): _dyn_str,
        Optional('style'): _dyn_str,
    }),
    _make_common_node('ImageSprite', {
        Required('mode'): _sprite_mode,
        Required('src'): _dyn_str,
    }),

    # GUI
    _make_gui_node('GuiRectangle', {
        Optional('background'): _dyn_str,
        Optional('border'): _dyn_str,
        Optional('html'): _dyn_str,
    }),

    # Grid
    _make_common_node('GridDebug', {
        Optional('size'): _dyn_num,
        Optional('divisions'): _dyn_num,
    }),

    # Cameras
    _make_common_node('PerspectiveCamera', {
        Optional('fov'): _dyn_num,
        Optional('near'): _dyn_num,
        Optional('far'): _dyn_num,
        Optional('look-at'): _dyn_vector3,
    }),

    # Controls
    _make_common_node('OrbitControls', {
        Optional('damping-factor'): _dyn_num,
        Optional('enabled'): _dyn_bool,
        Optional('enable-damping'): _dyn_bool,
        Optional('enable-pan'): _dyn_bool,
        Optional('enable-rotate'): _dyn_bool,
        Optional('enable-zoom'): _dyn_bool,
        Optional('key-pan-speed'): _dyn_num,
        Optional('max-azimuth-angle'): _dyn_num,
        Optional('max-distance'): _dyn_num,
        Optional('max-polar-angle'): _dyn_num,
        Optional('max-zoom'): _dyn_num,
        Optional('min-azimuth-angle'): _dyn_num,
        Optional('min-distance'): _dyn_num,
        Optional('min-polar-angle'): _dyn_num,
        Optional('min-zoom'): _dyn_num,
        Optional('pan-speed'): _dyn_num,
        Optional('rotate-speed'): _dyn_num,
        Optional('zoom-speed'): _dyn_num,
        Optional('screen-space-panning'): _dyn_bool,
    }),
    _make_common_node('PointerLockControls', {
        Optional('is-locked'): _dyn_bool,
        Optional('max-polar-angle'): _dyn_num,
        Optional('min-polar-angle'): _dyn_num,
        Optional('pointer-speed'): _dyn_num,
        Optional('target'): _dyn_expr,
    }),

    # Audio
    _make_common_node('Audio', {
        Required('filename'): str,
        Optional('loop'): bool,
        Optional('resumable'): bool,
        Optional('volume'): _dyn_num,
    }),

    # Queries
    # TODO: Raycaster
))


_schema = Schema({
    Required('ncjsam'): All(str, _validate_ncjsam),
    Required('package'): All(str, _validate_package),
    Optional('application'): _application_schema,
    Optional('entities'): Schema([_entity_schema])
})


def validate(module):
    return _schema(module)
