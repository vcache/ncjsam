from ncjsam.model.module.entities.subtree import Subtree
from ncjsam.model.module.entities.map import Map
from ncjsam.model.module.entities.reference import Reference

from ncjsam.model.module.entities.property import Variable
from ncjsam.model.module.entities.property import Constant
from ncjsam.model.module.entities.property import Function

from ncjsam.model.module.entities.trigger import Trigger

from ncjsam.model.module.entities.views import PlaneView
from ncjsam.model.module.entities.views import BoxView
from ncjsam.model.module.entities.views import SphereView
from ncjsam.model.module.entities.views import CapsuleView
from ncjsam.model.module.entities.views import CylinderView
from ncjsam.model.module.entities.views import ConeView
from ncjsam.model.module.entities.views import MeshView

from ncjsam.model.module.entities.lights import AmbientLight
from ncjsam.model.module.entities.lights import PointLight
from ncjsam.model.module.entities.lights import SpotLight

from ncjsam.model.module.entities.cameras import PerspectiveCamera

from ncjsam.model.module.entities.controls import OrbitControls

from ncjsam.model.module.entities.sprites import TextSprite
from ncjsam.model.module.entities.sprites import ImageSprite

from ncjsam.model.module.entities.gui import GuiRectangle

from ncjsam.model.module.entities.debuggers import GridDebug

from ncjsam.model.module.entities.audio import Audio


def get_registry():
    return [
        Subtree,
        Map,
        Reference,

        Variable,
        Constant,
        Function,

        Trigger,

        PlaneView,
        BoxView,
        SphereView,
        CapsuleView,
        CylinderView,
        ConeView,
        MeshView,

        AmbientLight,
        PointLight,
        SpotLight,

        PerspectiveCamera,

        OrbitControls,

        TextSprite,
        ImageSprite,

        GuiRectangle,

        GridDebug,

        Audio,
    ]
