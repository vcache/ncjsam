{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% macro update_light_parameter(name) -%}
            {% if name in common.dynamic_properties_names -%}
            this._light.{{ name }} = {{ common.eval_prop(name) }};
            {% endif %}
            {%- endmacro %}

            {{ update_light_parameter('color') }}
            {{ update_light_parameter('intensity') }}
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._light = new THREE.AmbientLight({{ common.eval_prop('color') }},
                                             {{ common.eval_prop('intensity') }});
        this._light.visible = this._visible;
        if (viewContainer) {
            viewContainer.add(this._light);
        }
        this.setTransformer(new {{ iter.class_name }}_Transformer(this._light, this));
    }

    onUnmerge() {
        this._light.removeFromParent();
        this._light.dispose();
        this._light = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._light.visible = visible;
    }
}
