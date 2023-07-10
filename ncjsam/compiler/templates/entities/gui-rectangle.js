{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if 'html' in common.dynamic_properties_names %}
            const html = {{ common.eval_prop('html') }};
            if (html !== this._html) {
                this._html = html;
                this._domElement.innerHTML = this._html;
            }
            {% endif %}

            {%
                if 'x' in common.dynamic_properties_names
                or 'y' in common.dynamic_properties_names
                or 'width' in common.dynamic_properties_names
                or 'height' in common.dynamic_properties_names
                or 'margin' in common.dynamic_properties_names
            %}
                this.recalcLayout();
            {% endif %}
        }
    }

    recalcLayout() {
        const x = ({{ common.eval_prop('x') }}).toLowerCase();
        const y = ({{ common.eval_prop('y') }}).toLowerCase();
        const width = ({{ common.eval_prop('width') }}).toLowerCase();
        const height = ({{ common.eval_prop('height') }}).toLowerCase();
        const margin = {{ common.eval_prop('margin') }};

        this._domElement.style.marginTop = `${margin.top}px`;
        this._domElement.style.marginRight = `${margin.right}px`;
        this._domElement.style.marginBottom = `${margin.bottom}px`;
        this._domElement.style.marginLeft = `${margin.left}px`;

        // width
        if (width.endsWith('px')) {
            const absValue = parseFloat(width);
            this._domElement.style.width = `${absValue}px`;
        } else if (width.endsWith('%')) {
            const relValue = parseFloat(width);
            this._domElement.style.width = `${relValue}%`;
        } else if (width == 'auto') {
            // TODO
        } else {
            throw new Error(`unexpected horizontal position: '${width}'`);
        }

        // height
        if (height.endsWith('px')) {
            const absValue = parseFloat(height);
            this._domElement.style.height = `${absValue}px`;
        } else if (height.endsWith('%')) {
            const relValue = parseFloat(height);
            this._domElement.style.height = `${relValue}%`;
        } else if (height == 'auto') {
            // TODO
        } else {
            throw new Error(`unexpected horizontal position: '${height}'`);
        }

        // x-coordinate
        if (x.endsWith('px')) {
            const absValue = parseFloat(x);
            this._domElement.style.left = `${absValue}px`;
        } else if (x.endsWith('%')) {
            var relValue = parseFloat(x) / 100.0;
            relValue *= (
                this._guiContainer.clientWidth - this._domElement.offsetWidth - (margin.right + margin.left)
            );
            this._domElement.style.left = `${relValue}px`;
        } else {
            throw new Error(`unexpected horizontal position: '${x}'`);
        }

        // y-coordinate
        if (y.endsWith('px')) {
            const absValue = parseFloat(y);
            this._domElement.style.top = `${absValue}px`;
        } else if (y.endsWith('%')) {
            var relValue = parseFloat(y) / 100.0;
            relValue *= (
                this._guiContainer.clientHeight - this._domElement.offsetHeight - (margin.bottom + margin.top)
            );
            this._domElement.style.top = `${relValue}px`;
        } else {
            throw new Error(`unexpected horizontal position: '${y}'`);
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._guiContainer = guiContainer;

        this._domElement = document.createElement('div');
        this._domElement.style.background = {{ common.eval_prop('background') }};
        this._domElement.style.border = {{ common.eval_prop('border') }};
        this._domElement.style.position = 'absolute';
        this._domElement.style.pointerEvents = {{ common.eval_prop('catch_input') }} ? 'auto' : 'none';
        this._domElement.style.visibility = this._visible ? 'visible'
                                                          : 'hidden';
        this._html = {{ common.eval_prop('html') }};
        this._domElement.innerHTML = this._html;
        this._guiContainer.appendChild(this._domElement);
        this.recalcLayout();
    }

    onResize(width, height) {
        this.recalcLayout();
    }

    onUnmerge() {
        this._guiContainer.removeChild(this._domElement);
        this._domElement = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        this._domElement.style.visibility = this._visible ? 'visible'
                                                          : 'hidden';
    }
}
