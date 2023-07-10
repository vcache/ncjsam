{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible || sync) {
            {% if 'data' in common.dynamic_properties_names %}
            if (this._data == null || sync || {{ common.eval_prop('update') }} ) {
                const data = {{ common.eval_prop('data') }};
                this.sync(data);
            }
            {% endif %}

            for(var key in this._children) {
                this._children[key].onStep(sync);
            }
        }
    }

    sync(data) {
        const nouveau = [];
        const revoked = [];
        
        for(var key in this._data) {
            if (!(key in data)) revoked.push(key);
        }
        for(var key in data) {
            if (!this._data || !(key in this._data)) nouveau.push(key);
        }

        for(var i in revoked) {
            const key = revoked[i];
            this._children[key].onUnmerge();
            delete this._children[key];
        }

        for(var key in this._children) {
            this._children[key].setContextValue('{{ iter.variable }}', data[key]);
        }

        for(var i in nouveau) {
            const key = nouveau[i];
            this._children[key] = new {{ iter.element.class_name }}(
                '{{ iter.element.id }}', '{{ iter.element.path.as_string() }}', // TODO maybe 'key' instead 'child.id'
                this._assetsManager, this);

            this._children[key].setContextValue('{{ iter.variable }}', data[key]);
            this._children[key].onEmerge(this._group, this._guiContainer);
        }

        this._data = data;
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._guiContainer = guiContainer;
        this._group = new THREE.Group();
        this._group.visible = this._visible;
        if (viewContainer) {
            viewContainer.add(this._group);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._group, this));
        this._data = null;
        this._children = {};
    }

    onUnmerge() {
        for(var key in this._children) {
            this._children[key].onUnmerge();
        }
        this._children = {}
        this._data = null
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
        // NOTE: not registering children since they are dynamic,
        //       and call to registerEntity have done once on load,
        //       they may be accessed through two-pass access, ie:
        //       $['/foo/bar']['child-id']
    }

    dump() {
        const children = {}
        for(var key in  this._children) {
            children[key] = this._children[key].dump();
        }
        return {
            ...super.dump(),
            'map': {
                'data': this._data,
                'children': children,
            },
        };
    }

    restore(state_dump) {
        // TODO: validate state_dump
        super.restore(state_dump);
        const map_state = state_dump['map'];
        this.sync(map_state['data']);
        for(var key in map_state['children']) {
            const child_state = map_state['children'][key];
            this._children[key].restore(child_state);
        }
    }
}
