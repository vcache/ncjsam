{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    constructor(entity_id, full_path, assetsManager, parent) {
        super(entity_id, full_path, assetsManager, parent);
        this._children = [
            {% for child in iter.children %}
            new {{ child.class_name }}(
                '{{ child.id }}', '{{ child.path.as_string() }}',
                assetsManager, this),
            {% endfor %}
        ];
    }

    onStep(sync) {
        super.onStep(sync);
        if (this._visible || sync) {
            for(var key in this._children) {
                this._children[key].onStep(sync);
            }
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._group = new THREE.Group();
        this._group.visible = this._visible;
        if (viewContainer) {
            viewContainer.add(this._group);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._group, this));
        this._subscribedEvents = new Set();
        for(var key in this._children) {
            this._children[key].onEmerge(this._group, guiContainer);
            for(const kind of this._children[key].getSubscribedEvents()) {
                this._subscribedEvents.add(kind);
            }
        }
    }

    onUnmerge() {
        for(var key in this._children) {
            this._children[key].onUnmerge();
        }
        this._group.removeFromParent();
        this._group = null;
        super.onUnmerge();
    }

    onResize(width, height) {
        for(var key in this._children) {
            this._children[key].onResize(width, height);
        }
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._group.visible = visible;
        for(var key in this._children) {
            this._children[key].onVisibleChanged(visible);
        }
    }

    onEventPosted(kind, args) {
        if (this._subscribedEvents.has(kind)) {
            for(var key in this._children) {
                this._children[key].onEventPosted(kind, args);
            }
        }
    }

    getSubscribedEvents() {
        return this._subscribedEvents;
    }

    query(target, params) {
        // TODO: this gaves pretty random result (and non-deterministic in general)
        //       should be weighted somehow according to user-provided hints
        for(var key in this._children) {
            const result = this._children[key].query(target, params);
            if (result) return result;
        }
        return null;
    }

    registerEntity(destination_object) {
        super.registerEntity(destination_object);
        for(var key in this._children) {
            this._children[key].registerEntity(destination_object);
        }
    }

    dump() {
        const children = {};
        for(var key in this._children) {
            const child = this._children[key];
            children[key] = child.dump();
        }
        return {
            ...super.dump(),
            'subtree-children': children,
        };
    }

    restore(state_dump) {
        // TODO: validate state_dump
        super.restore(state_dump);
        for(var key in state_dump['subtree-children']) {
            const child_state = state_dump['subtree-children'][key];
            this._children[key].restore(child_state);
        }
    }
}
