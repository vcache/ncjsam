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

    getTarget() {
        {% if 'target' in iter.properties -%}
        return {{ common.eval_prop('target') }};
        {% else %}
        return $.camera();
        {% endif %}
    }

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            const camera = this.getTarget();

            if (this._controls && camera &&
                this._controls.getObject().id != camera.id)
            {
                this.onUnmerge();
            }

            if (!this._controls && camera) {
                this.onEmerge(); // TODO: wtf?? where is parameters??
            }

            if (this._controls && camera) {
                {{ update_controls_parameter('is_locked') }}
                {{ update_controls_parameter('max_polar_angle') }}
                {{ update_controls_parameter('min_polar_angle') }}
                {{ update_controls_parameter('pointer_speed') }}
            }
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        const camera = this.getTarget();
        const renderer = $.renderer();
        if (camera && renderer) {
            this._controls = new PointerLockControls(camera, renderer.domElement);
            this._controls.enabled = this._visible;
            {{ setup_controls_parameter('is_locked') }}
            {{ setup_controls_parameter('max_polar_angle') }}
            {{ setup_controls_parameter('min_polar_angle') }}
            {{ setup_controls_parameter('pointer_speed') }}
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
            result['pointer-lock-controls'] = {}
        }
        return result;
    }

    restore(state_dump) {
        super.restore(state_dump);
    }
}
