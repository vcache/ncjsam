{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if 'volume' in common.dynamic_properties_names %}
            const volume = {{ common.eval_prop('volume') }};
            if (volume != this._volume) {
                this._audio.volume = volume;
                this._volume = volume;
            }
            {% endif %}
        }
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._audio = new Audio({{ common.eval_prop('filename') }});
        this._audio.loop = {{ common.eval_prop('loop') }};
        this._audio.volume = {{ common.eval_prop('volume') }};
        this._visible = false;
        this._volume = this._audio.volume;
    }

    onUnmerge() {
        this._audio.pause();
        this._audio = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        if (visible) {
            this._audio.play();
        } else {
            this._audio.pause();
            const resumable = {{ common.eval_prop('resumable') }};
            if (!resumable) {
                this._audio.fastSeek(0);
            }
        }
    }
}
