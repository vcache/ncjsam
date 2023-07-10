from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

from ncjsam.model.etc import UnJson


@dataclass
class MetaInfo:
    title: str = 'Untitled NCJSAM Game'
    version: str = '0.1'
    authors: List[str] = field(default_factory=list)
    description: Optional[str] = None

    @staticmethod
    def deserialize(data):
        return UnJson(data).done(MetaInfo)


@dataclass
class Render:
    debug_physics: bool = False

    @staticmethod
    def deserialize(data):
        return UnJson(data).done(Render)


class WindowMode(Enum):
    FULLSCREEN = 1
    WINDOWED = 2

    @staticmethod
    def deserialize(data):
        return WindowMode[data.upper()]


"""
TODO:
    window-mode:
        fullscreen: {}
    window-mode:
        windowed:
            resizable: true
            # initial: maximized
            initial:
                width: 1024
                height: 768
"""


@dataclass
class Window:
    title: str = 'Untitled NCJSAM Game'
    mode: WindowMode = WindowMode.WINDOWED
    resizable: bool = True

    @staticmethod
    def deserialize(data):
        return (UnJson(data).replace('mode', WindowMode.deserialize)
                            .done(Window))


@dataclass
class Application:
    meta_info: MetaInfo = MetaInfo()
    render: Render = Render()
    window: Window = Window()

    @staticmethod
    def deserialize(data):
        return (UnJson(data).replace('meta-info', MetaInfo.deserialize)
                            .replace('render', Render.deserialize)
                            .replace('window', Window.deserialize)
                            .done(Application))
