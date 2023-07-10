{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if ('radius' in common.dynamic_properties_names) or
                  ('length' in common.dynamic_properties_names) %}
            const radius = {{ common.eval_prop('radius') }};
            const length = {{ common.eval_prop('length') }};
            if (radius != this._radius || length != this._length) {
                const viewContainer = this._mesh.parent;
                this.onUnmerge();
                this._radius = radius;
                this._length = length;
                this.onEmerge(viewContainer. null);
            }
            {% endif %}
            this.recalcMaterialProps(this._mesh.material);
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        if (!this._radius) this._radius = {{ common.eval_prop('radius') }};
        if (!this._length) this._length = {{ common.eval_prop('length') }};
        this._geometry = new THREE.CapsuleGeometry(this._radius,
                                                   this._length);
        this._material = this.buildMaterial();
        this._mesh = new THREE.Mesh(this._geometry, this._material);
        this._mesh.userData = {
            'treeNode': this,
        }
        this._mesh.visible = this._visible;
        if (viewContainer) { // TODO: move to base class
            viewContainer.add(this._mesh);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._mesh, this));
    }

    onUnmerge() {
        this._radius = null;
        this._length = null;
        this._mesh.removeFromParent();
        this._mesh = null;
        this._geometry.dispose();
        this._geometry = null;
        this._material.dispose();
        this._material = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._mesh.visible = visible;
    }
}
