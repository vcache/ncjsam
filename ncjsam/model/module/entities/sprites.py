from dataclasses import dataclass

from ncjsam.model.etc import Path
from ncjsam.model.module.entity import Entity

from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_str


@dataclass
class TextSprite(Entity):
    mode: str = None  # TODO: NOTE-A
    text: type_dyn_str = None  # TODO: NOTE-A
    style: type_dyn_str = None  # TODO: NOTE-A

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/sprite.js',
            'element': 'div',
        })
        result[0]['properties'].update({
            'mode': render_property(self.mode),
            'text': render_property(self.text),
            'style': render_property(self.style),
        })
        return result


@dataclass
class ImageSprite(Entity):
    mode: str = None  # TODO: NOTE-A
    src: type_dyn_str = None  # TODO: NOTE-A

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/sprite.js',
            'element': 'img',
        })
        result[0]['properties'].update({
            'mode': render_property(self.mode),
            'src': render_property(self.src),
        })
        return result
