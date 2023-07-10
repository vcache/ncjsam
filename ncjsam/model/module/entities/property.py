from dataclasses import dataclass
from typing import Any

from ncjsam.model.module.entity import Entity
from ncjsam.model.types import render_property
from ncjsam.model.etc import Path


@dataclass
class Variable(Entity):
    default_value: Any = None  # TODO: NOTE-A
    # TODO: on-change action

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/variable-entity.js',
        })
        result[0]['properties'].update({
            'default_value': render_property(self.default_value),
        })
        return result


@dataclass
class Constant(Entity):
    default_value: Any = None  # TODO: NOTE-A

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/constant-entity.js',
        })
        result[0]['properties'].update({
            'default_value': render_property(self.default_value),
        })
        return result


@dataclass
class Function(Entity):
    expression: Any = None  # TODO: NOTE-A

    @classmethod
    def deserialize(cls, data):
        return (cls.unjson(data).done(cls))

    def compile(self, parent_path: Path):
        result = super().compile(parent_path=parent_path)
        assert len(result) == 1
        result[0].update({
            'template_file': 'entities/function-entity.js',
        })
        result[0]['properties'].update({
            'expression': render_property(self.expression),
        })
        return result
