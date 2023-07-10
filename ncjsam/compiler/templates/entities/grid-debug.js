{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    {% set maybe_reemerge = ('size' in common.dynamic_properties_names) or
                            ('divisions' in common.dynamic_properties_names) %}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if maybe_reemerge %}
            const size = {{ common.eval_prop('size') }};
            const divisions = {{ common.eval_prop('divisions') }};
            if (size != this._size || divisions != this._divisions) { // TODO: don't compare static props
                const viewContainer = this._mesh.parent;
                this._size = size;
                this._divisions = divisions;
                this.onUnmerge();
                this.onEmerge(viewContainer, null);
            }
            {% endif %}
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        if (!this._size) this._size = {{ common.eval_prop('size') }};
        if (!this._divisions) this._divisions = {{ common.eval_prop('divisions') }};
        this._helper = new THREE.GridHelper(this._size,
                                            this._divisions);
        this._helper.name = this.getFullPath();
        this._helper.userData = {
            'treeNode': this,
        }
        this._helper.visible = this._visible;
        if (viewContainer) {
            viewContainer.add(this._helper);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._helper, this));
    }

    onUnmerge() {
        this._size = null;
        this._divisions = null;
        this._helper.removeFromParent();
        this._helper.dispose();
        this._helper = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._helper.visible = visible;
    }
}
