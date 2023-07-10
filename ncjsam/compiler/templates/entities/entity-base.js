class EntityBase {
    constructor(entity_id, full_path, assetsManager, parent) {
        this._entity_id = entity_id;
        this._full_path = full_path;
        this._assetsManager = assetsManager;
        this._parent = parent;
        // TODO: transfer context value from parent if any
    }

    // TODO: maybe property?
    setContextValue(variable_name, variable_data) {
        // TODO: filter builtin names
        this[variable_name] = variable_data;
        if (this._transformer) {
            this._transformer[variable_name] = variable_data;
        }
        this._name_of_variable_name = variable_name;
    }

    setTransformer(transformer) {
        this._transformer = transformer;
        if (this._transformer) {
            if (this._name_of_variable_name) {
                this._transformer[this._name_of_variable_name] = this[this._name_of_variable_name];
            }
            this._transformer.initValues();
        }
    }

    onStep(sync) /* virtual */ {
        const visible = this.evalProperty__visible(); // TODO: dont' evaluate when 'visible' is static
        if (visible != this._visible) {     // TODO: don't need to eval this on every iteration
            this.onVisibleChanged(visible);
        }
        if (visible && this._transformer) {
            this._transformer.updateValues();
        }
        // TODO: prune the tree (i.e. when all descendants are static entities)
    }

    onEmerge(viewContainer, guiContainer) /* virtual */ {
        this._visible = this.evalProperty__visible();
    }
    
    onUnmerge() /* virtual */ {
        this._visible = null;
        this._transformer = null;
        this[this._name_of_variable_name] = null;
        this._name_of_variable_name = null;
    }

    onResize(width, height) /* virtual */ {}
    
    onVisibleChanged(visible) /* virtual */ {
        this._visible = visible;
    }

    onEventPosted(kind, args) /* virtual */ {}

    getSubscribedEvents() /* virtual */ { return new Set(); }

    query(target, params) /* virtual */ { return null; }

    getFullPath() { return this._full_path; }

    getEntityId() { return this._entity_id; }

    registerEntity(destination_object) /* virtual */ {
        destination_object[this._full_path] = this;    // TODO: put wrapper instead 'this'
    }

    dump() {
        const result = {
            'entity-id': this._entity_id,
            'full-path': this.getFullPath(),
            'visible': this._visible, //  TODO: maybe useless?
        };
        if (this._name_of_variable_name) {
            result['context-value'] = {
                'name': this._name_of_variable_name,
                'value': this[this._name_of_variable_name],
            };
        }
        return result;
    }

    restore(state_dump) {
        // TODO: validate state_dump
        this._visible = state_dump['visible'];
        const contextValue =  state_dump['context-value'];
        if (contextValue) {
            this.setContextValue(contextValue['name'],
                                 contextValue['value']);
        }
    }
}
