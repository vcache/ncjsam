{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    {% set maybe_dynamic_reemerge = ('fov' in common.dynamic_properties_names)
                                 or ('near' in common.dynamic_properties_names)
                                 or ('far' in common.dynamic_properties_names) %}

    {% macro update_camera_parameter(name) -%}
    {% if name in common.dynamic_properties_names -%}
    this._camera.{{ name }} = {{ common.eval_prop(name) }};
    {% endif %}
    {%- endmacro %}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if maybe_dynamic_reemerge %}
            {{ update_camera_parameter('fov') }}
            {{ update_camera_parameter('near') }}
            {{ update_camera_parameter('far') }}
            this._camera.updateProjectionMatrix();
            {% endif %}

            {% if 'look_at' in common.dynamic_properties_names %}
            this._camera.lookAt({{ common.eval_prop('look_at') }});
            {% endif %}
        }
    }

    onResize(width, height) {
        super.onResize(width, height);
        this._camera.aspect = width / height;
        this._camera.updateProjectionMatrix();
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._camera = new THREE.PerspectiveCamera({{ common.eval_prop('fov') }},
                                                   $.width() / $.height(),
                                                   {{ common.eval_prop('near') }},
                                                   {{ common.eval_prop('far') }});
        this._camera.visible = this._visible;
        if (viewContainer) {
            viewContainer.add(this._camera);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._camera, this));

        {% if 'look_at' in iter.properties %}
        this._camera.lookAt({{ common.eval_prop('look_at') }});
        {% endif %}
    }

    onUnmerge() {
        this._camera.removeFromParent();
        this._camera = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._camera.visible = visible;
    }

    query(target, params) { return (target == 'camera') ? this._camera : null; }

    dump() {
        // NOTE: these only need correctly dump/restore a Camera that controlled via *Controls
        return {
            ...super.dump(),
            'perspective-camera': this._camera.toJSON(null),
        };
    }

    restore(state_dump) {
        super.restore(state_dump);
        const camera_dump = state_dump['perspective-camera'].object;

        this._camera.aspect = camera_dump.aspect;
        this._camera.far = camera_dump.far;
        this._camera.filmGauge = camera_dump.filmGauge;
        this._camera.filmOffset = camera_dump.filmOffset;
        this._camera.focus = camera_dump.focus;
        this._camera.fov = camera_dump.fov;
        //this._camera.layers: 1
        this._camera.near = camera_dump.near;
        this._camera.zoom = camera_dump.zoom;

        const matrix = new THREE.Matrix4();
        matrix.fromArray(camera_dump.matrix);
        this._camera.matrixAutoUpdate = false;
        this._camera.matrix = new THREE.Matrix4();
        this._camera.applyMatrix4(matrix);
        this._camera.matrixAutoUpdate = true;
    }
}
