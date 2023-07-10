from dataclasses import dataclass

from ncjsam.model.etc import Path
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_num
from ncjsam.model.module.entity import Entity


@dataclass
class Audio(Entity):
    filename: str = None  # SEE NOTE-A
    loop: bool = False
    resumable: bool = False
    volume: type_dyn_num = .7

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/audio.js',
        })
        result[0]['properties'].update({
            'filename': render_property(self.filename),
            'loop': render_property(self.loop),
            'resumable': render_property(self.resumable),
            'volume': render_property(self.volume),
        })
        return result
