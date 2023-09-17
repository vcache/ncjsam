{% import 'entities/common-macros.jinja' as common with context %}
{% include 'entities/transformer.js' %}

class {{ iter.class_name }} extends EntityBase {
    {{ common.generate_properties() }}
    {{ common.generate_materials() }}

    onStep(sync) {
        super.onStep(sync);
        if (this._visible) {
            {% if 'filename' in common.dynamic_properties_names %}
            const filename = {{ common.eval_prop('filename') }};
            if (filename != this._filename) {
                this.onUnmerge();
                this._filename = filename;
                this.onEmerge(this._viewContainer, null);
            }
            {% endif %}

            {% if 'animation' in common.dynamic_properties_names %}
            const animation = {{ common.eval_prop('animation') }};
            if (animation != this._animation) {
                if (animation) {
                    this.playAnimation(animation, THREE.LoopRepeat);
                } else {
                    this.resetAnimation();
                }
                this._animation = animation;
            }
            {% endif %}

            if (this._mixer) {
                this._mixer.update($.dt());
            }
        }
    }

    listAnimations() {
        const result = [];
        for(var i in this._animations) {
            result.push(this._animations[i].name);
        }
        return result;
    }

    // THREE.LoopOnce | THREE.LoopRepeat | THREE.LoopPingPong
    playAnimation(animation, loop = THREE.LoopOnce) {
        if (this._mixer) {
            const clip = THREE.AnimationClip.findByName(this._animations, animation);
            if (clip) {
                const action = this._mixer.clipAction(clip);
                action.reset();
                action.loop = loop;
                action.play();
            } else {
                console.log(`no such animation clip: ${animation}`);
            }
        }
    }

    resetAnimation() {
        this._mixer.stopAllAction();
    }

    onEmerge(viewContainer, guiContainer) {
        super.onEmerge(viewContainer, guiContainer);
        this._viewContainer = viewContainer;
        if (this._visible) {
            if (!this._filename) this._filename = {{ common.eval_prop('filename') }};
            const asset = this._assetsManager.getAsset(this._filename);
            if (!asset) throw Error(`no such mesh: ${this._filename}`)
            this._scene = asset.scene.clone();

            this._scene.userData = {
                'treeNode': this,
            }
            for(var i in this._scene.children) {
                this._scene.children[i].userData = {
                    'treeNode': this,
                }
            }

            this._scene.visible = this._visible;
            if (viewContainer) { // TODO: move to base class
                viewContainer.add(this._scene);
            }
            this.setTransformer(new {{ iter.class_name }}_Transformer(this._scene, this));

            // NOTE: disable "Group by NLA Track"
            if (asset.animations.length > 0) {
                this._mixer = new THREE.AnimationMixer(this._scene);
                this._animations = asset.animations;
            } else {
                this._mixer = null;
            }

            this._animation = {{ common.eval_prop('animation') }};
            if (this._animation) {
                this.playAnimation(this._animation, THREE.LoopRepeat);
            }
        }
    }

    onUnmerge() {
        this._filename = null;
        if (this._scene) {
            this._scene.removeFromParent();
        }
        this._scene = null;
        super.onUnmerge();
    }

    onVisibleChanged(visible) {
        super.onVisibleChanged(visible);
        if (this._scene) {
            this._scene.visible = visible;
        }
    }
}
