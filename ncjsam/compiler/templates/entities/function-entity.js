{% import 'entities/common-macros.jinja' as common with context %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
    }

    get value() {
        return {{ common.eval_prop('expression') }};
    }
}
