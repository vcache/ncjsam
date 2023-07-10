{% import 'entities/common-macros.jinja' as common with context %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._subscribedEvents = new Set([{% for i in iter.events %}'{{ i }}',{% endfor %}]);
    }

    onEventPosted(kind, args) {
        this.event = {
            'kind': kind,
            'args': args,
        };
        if (this._subscribedEvents.has(kind) && {{ common.eval_prop('condition') }}) {
            {{ iter.action.expr | indent(12) }};
        }
        this.event = null;
    }

    getSubscribedEvents() { return this._subscribedEvents; }
}
