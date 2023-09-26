{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    {% macro update_controls_parameter(name) -%}
    {% if name in common.dynamic_properties_names -%}
    this._controls.{{ name | ncjsam_snake_to_camel }} = {{ common.eval_prop(name) }};
    {% endif %}
    {%- endmacro %}

    {% macro setup_controls_parameter(name) -%}
    {% if name in iter.properties -%}
    this._controls.{{ name | ncjsam_snake_to_camel }} = {{ common.eval_prop(name) }};
    {% endif %}
    {%- endmacro %}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            const camera = $.camera();

            if (this._controls && camera &&
                this._controls.object.id != camera.id)
            {
                this.onUnmerge();
            }

            if (!this._controls && camera) {
                this.onEmerge(); // TODO: wtf?? where is parameters??
            }

            if (this._controls && camera) {
                {{ update_controls_parameter('damping_factor') }}
                {{ update_controls_parameter('enable_damping') }}
                {{ update_controls_parameter('enable_pan') }}
                {{ update_controls_parameter('enable_rotate') }}
                {{ update_controls_parameter('enable_zoom') }}
                {{ update_controls_parameter('key_pan_speed') }}
                {{ update_controls_parameter('max_azimuth_angle') }}
                {{ update_controls_parameter('max_distance') }}
                {{ update_controls_parameter('max_polar_angle') }}
                {{ update_controls_parameter('max_zoom') }}
                {{ update_controls_parameter('min_azimuth_angle') }}
                {{ update_controls_parameter('min_distance') }}
                {{ update_controls_parameter('min_polar_angle') }}
                {{ update_controls_parameter('min_zoom') }}
                {{ update_controls_parameter('pan_speed') }}
                {{ update_controls_parameter('rotate_speed') }}
                {{ update_controls_parameter('zoom_speed') }}
                this._controls.update();
            }
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        const camera = $.camera();
        const renderer = $.renderer();
        if (camera && renderer) {
            this._controls = new OrbitControls(camera, renderer.domElement);
            this._controls.enabled = this._visible;
            {{ setup_controls_parameter('damping_factor') }}
            {{ setup_controls_parameter('enable_damping') }}
            {{ setup_controls_parameter('enable_pan') }}
            {{ setup_controls_parameter('enable_rotate') }}
            {{ setup_controls_parameter('enable_zoom') }}
            {{ setup_controls_parameter('key_pan_speed') }}
            {{ setup_controls_parameter('max_azimuth_angle') }}
            {{ setup_controls_parameter('max_distance') }}
            {{ setup_controls_parameter('max_polar_angle') }}
            {{ setup_controls_parameter('max_zoom') }}
            {{ setup_controls_parameter('min_azimuth_angle') }}
            {{ setup_controls_parameter('min_distance') }}
            {{ setup_controls_parameter('min_polar_angle') }}
            {{ setup_controls_parameter('min_zoom') }}
            {{ setup_controls_parameter('pan_speed') }}
            {{ setup_controls_parameter('rotate_speed') }}
            {{ setup_controls_parameter('zoom_speed') }}

            if (this._pended_restore) {
                this._controls.target.fromArray(this._pended_restore.target);
                this._pended_restore = null;
            }
        }
    }

    onUnmerge() {
        if (this._controls) {
            this._controls.dispose();
            this._controls = null;
        }
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        if (this._controls) {
            this._controls.enabled = visible;
        }
    }

    dump() {
        const result = {
            ...super.dump(),

        };
        if (this._controls) {
            result['orbit-controls'] = {
                'target': this._controls.target.toArray(),
            }
        }
        return result;
    }

    restore(state_dump) {
        super.restore(state_dump);
        this._pended_restore = state_dump['orbit-controls'];
    }
}
