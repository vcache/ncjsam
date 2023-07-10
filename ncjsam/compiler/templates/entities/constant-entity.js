{% import 'entities/common-macros.jinja' as common with context %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._value = {{ common.eval_prop('default_value') }};
    }

    get value() { return this._value; }

    dump() {
        // TODO: not sure if constants should be saved and restored
        //       for obvious "cons": they'll become immutable event when changed via YAML
        return {
            ...super.dump(),
            'constant-value': this._value,
        };
    }

    restore(state_dump) {
        // TODO: validate state_dump
        //super.restore(state_dump);
        //this._value = state_dump['constant-value']
    }
}
