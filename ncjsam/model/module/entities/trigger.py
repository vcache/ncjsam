from dataclasses import dataclass
from typing import List, Optional

from ncjsam.model.module.entity import Entity
from ncjsam.model.types import render_property
from ncjsam.model.types import type_dyn_bool
from ncjsam.model.types import Expr
from ncjsam.model.etc import Path


@dataclass
class Trigger(Entity):
    events: List[str] = None    # TODO: NOTE-A
    action: Expr = None         # TODO: NOTE-A
    condition: Optional[type_dyn_bool] = True

    @classmethod
    def deserialize(cls, data):
        return cls.unjson(data).done(cls)

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/trigger-entity.js',
            'events': self.events,
            'action': self.action.compile(),
        })
        result[0]['properties'].update({
            'condition': (
                render_property(self.condition) if self.condition else True
            ),
        })

        return result
