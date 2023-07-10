{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {

            {# DIV BEGIN #}
            {% if iter.element == 'div' %}
            {% if 'text' in common.dynamic_properties_names %}
            const text = {{ common.eval_prop('text') }};
            if (text !== this._text) {
                this._text = text;
                this._domElement.textContent = text;
            }
            {% endif %}

            {% if 'style' in common.dynamic_properties_names %}
            const style = {{ common.eval_prop('style') }};
            if (style !== this._style) {
                this._style = style;
                this._domElement.style.cssText = style;
            }
            {% endif %}
            {% endif %}
            {# DIV END #}
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._domElement = document.createElement('{{ iter.element }}');

        {% if iter.element == 'div' %}
        if (!this._text) this._text = {{ common.eval_prop('text') }};
        if (!this._style) this._style = {{ common.eval_prop('style') }};
        this._domElement.textContent = this._text;
        this._domElement.style.cssText = this._style;
        {% elif iter.element == 'img' %}
        if (!this._src) this._src = {{ common.eval_prop('src') }};
        this._domElement.src = this._src;
        {% else %}
        throw new Error('bad element type: {{ iter.element }}')
        {% endif %}

        const mode = {{ common.eval_prop('mode') }};
        if (mode === '2d') {
            this._cssObject = new CSS2DObject(this._domElement);
        } else if (mode === '3d-faced') {
            this._cssObject = new CSS3DSprite(this._domElement);
        } else if (mode === '3d') {
            this._cssObject = new CSS3DObject(this._domElement);
        } else {
            throw new Error(`unknown sprite mode: ${mode}`);
        }
        this._cssObject.visible = this._visible;

        if (viewContainer) { // TODO: move to base class
            viewContainer.add(this._cssObject);
        }

        this.setTransformer(new {{ iter.class_name }}_Transformer(this._cssObject, this));
    }

    onUnmerge() {
        this._cssObject.removeFromParent();
        this._cssObject = null;
        this._domElement = null;
        this._text = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._cssObject.visible = visible;
    }
}
