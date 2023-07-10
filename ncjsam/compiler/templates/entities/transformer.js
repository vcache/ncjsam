{% set translate = iter.get('transformation', {}).translate %}
{% set euler_angles = iter.get('transformation', {}).euler_angles %}
{% set axis_angle = iter.get('transformation', {}).axis_angle %}
{% set quaternion = iter.get('transformation', {}).quaternion %}
{% set scale = iter.get('transformation', {}).scale %}
{% set trivial = translate is undefined and euler_angles is undefined and
                 axis_angle is undefined and quaternion is undefined and
                 scale is undefined %}

class {{ iter.class_name }}_Transformer {
    static kTrivial = {{ 'true' if trivial else 'false' }};
    static kStatic = {{ 
        'true' if ((translate is defined and translate.expr is undefined) or
                   (euler_angles is defined and euler_angles.expr is undefined) or
                   (axis_angle is defined and axis_angle.expr is undefined) or
                   (quaternion is defined and quaternion.expr is undefined) or
                   (scale is defined and scale.expr is undefined) or trivial)
        else 'false'
    }};

    constructor(object, entity) {
        this._object = object;
        this._entity = entity;
    }

    initValues() {
        this.eval_statics();
        this.eval_dynamics();
    }

    updateValues() {
        this.eval_dynamics();
    }

    eval_statics() {
        {# /* TRANSLATE */ #}
        {% if translate is defined and translate.expr is undefined %}
        this._object.position.set({{ translate['vector3d'] | join(', ') }});
        {% endif %}
        {# /* EULER ANGLES */ #}
        {% if euler_angles is defined and euler_angles.expr is undefined %}
        this._object.setRotationFromEuler(new THREE.Euler({{ euler_angles['vector3d'] | join(', ') }}, 'XYZ'));
        {% endif %}
        {# /* AXIS ANGLE */ #}
        {% if axis_angle is defined and axis_angle.expr is undefined %}
        this._object.setRotationFromAxisAngle(
            new THREE.Vector({{ axis_angle | slice(3) | join(', ') }}),
            {{ axis_angle[3] }});
        {% endif %}
        {# /* QUATERNION */ #}
        {% if quaternion is defined and quaternion.expr is undefined %}
        this._object.setRotationFromQuaternion(new THREE.Quaternion({{ quaternion | join(', ') }}));
        {% endif %}
        {# /* SCALE */ #}
        {% if scale is defined and scale.expr is undefined %}
        this._object.scale.set({{ scale['vector3d'] | join(', ') }});
        {% endif %}
    }

    eval_dynamics() {
        {# /* TRANSLATE */ #}
        {% if translate is defined and translate.expr is defined %}
        const translateExpr = () => {
            {{ translate.expr | indent(12) }}
        }
        this._object.position.copy(translateExpr());
        {% endif %}
        {# /* EULER ANGLES */ #}
        {% if euler_angles is defined and euler_angles.expr is defined %}
        const eulerAnglesExpr = () => {
            {{ euler_angles.expr | indent(12) }}
        }
        this._object.setRotationFromEuler(eulerAnglesExpr(), 'XYZ');
        {% endif %}
        {# /* AXIS ANGLE */ #}
        {% if axis_angle is defined and axis_angle.expr is defined %}
        const axisAngle = (() => {
            {{ axis_angle.expr | indent(12) }}
        })();
        const axis = new THREE.Vector3(axisAngle.x, axisAngle.y, axisAngle.z);
        axis.normalize();
        this._object.setRotationFromAxisAngle(axis, axisAngle.w);
        {% endif %}
        {# /* QUATERNION */ #}
        {% if quaternion is defined and quaternion.expr is defined %}
        const quaternionExpr = () => {
            {{ quaternion.expr | indent(12) }}
        }
        this._object.setRotationFromQuaternion({{ quaternionExpr() }});
        {% endif %}
        {# /* SCALE */ #}
        {% if scale is defined and scale.expr is defined %}
        const scaleExpr = () => {
            {{ scale.expr | indent(12) }}
        }
        this._object.scale.copy(scaleExpr());
        {% endif %}
    }

    // API to mimic Entity

    getFullPath() { return this._entity._full_path; }

    getEntityId() { return this._entity._entity_id; }
}