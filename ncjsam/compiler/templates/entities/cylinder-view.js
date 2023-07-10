{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if ('top_radius' in common.dynamic_properties_names) or
                  ('bottom_radius' in common.dynamic_properties_names) or
                  ('height' in common.dynamic_properties_names) %}
            const top_radius = {{ common.eval_prop('top_radius') }};
            const bottom_radius = {{ common.eval_prop('bottom_radius') }};
            const height = {{ common.eval_prop('height') }};
            if (top_radius != this._top_radius ||
                bottom_radius != this._bottom_radius ||
                height != this._height)
            {
                const viewContainer = this._mesh.parent;
                this.onUnmerge();
                this._top_radius = top_radius;
                this._bottom_radius = bottom_radius;
                this._height = height;
                this.onEmerge(viewContainer, null);
            }
            {% endif %}
            this.recalcMaterialProps(this._mesh.material);
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        if (!this._top_radius) this._top_radius = {{ common.eval_prop('top_radius') }};
        if (!this._bottom_radius) this._bottom_radius = {{ common.eval_prop('bottom_radius') }};
        if (!this._height) this._height = {{ common.eval_prop('height') }};
        this._geometry = new THREE.CylinderGeometry(this._top_radius,
                                                    this._bottom_radius,
                                                    this._height);
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
        this._top_radius = null;
        this._bottom_radius = null;
        this._height = null;
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
