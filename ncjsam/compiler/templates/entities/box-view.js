{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if 'dimensions' in common.dynamic_properties_names %}
            const dimensions = {{ common.eval_prop('dimensions') }};
            if (!dimensions.equals(this._dimensions)) {
                const viewContainer = this._mesh.parent;
                this.onUnmerge();
                this._dimensions = dimensions;
                this.onEmerge(viewContainer, null);
            }
            {% endif %}
            this.recalcMaterialProps(this._mesh.material);
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        if (!this._dimensions) this._dimensions = {{ common.eval_prop('dimensions') }};
        this._geometry = new THREE.BoxGeometry(this._dimensions.x,
                                               this._dimensions.y,
                                               this._dimensions.z);
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
        this._dimensions = null;
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
