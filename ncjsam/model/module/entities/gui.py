from dataclasses import dataclass
from typing import Optional

from ncjsam.model.etc import Path
from ncjsam.model.types import Layout
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_str
from ncjsam.model.module.entity import Entity


@dataclass
class GuiRectangle(Entity):
    layout: Optional[Layout] = None  # TODO: move to GuiBase class
    background: Optional[type_dyn_str] = 'red'
    border: Optional[type_dyn_str] = ''
    html: Optional[type_dyn_str] = None
    catch_input: Optional[bool] = False

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).replace('layout', Layout.deserialize)
                                .done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/gui-rectangle.js',
        })
        result[0]['properties'].update({
            'background': render_property(self.background),
            'border': render_property(self.border),
            'html': render_property(self.html),
            'catch_input': render_property(self.catch_input),
            # TODO: hack due to flat structure of properties
            **render_property(self.layout),
        })
        return result
