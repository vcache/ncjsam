/*
{% include 'common-header.jinja' %}

*/

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// TODO: these are optional, don't include when not required
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';
import { CSS3DRenderer, CSS3DObject, CSS3DSprite } from 'three/addons/renderers/CSS3DRenderer.js';

/* API class */

class API {
    constructor() { }

    __setMain(main) { this._main = main; }

    timestamp = () => { return this._main.getWallclock(); }
    dt = () => { return this._main.getLastDt(); }
    camera = () => { return this._main.getCamera(); }
    renderer = () => { return this._main.getRenderer(); }
    width = () => { return window.innerWidth; }
    height = () => { return window.innerHeight; }
    enqueue = (kind, args) => { this._main.enqueue(kind, args); }

    play = (filename, volume) => {
        const sound = new Audio(filename);
        sound.volume = volume;
        return sound.play();
    }

    pointerIntersections = () => {
        return this._main.getPointerIntersections();
    }
}

const $ = new API();

/* Generated classes */

{% include 'entities/entity-base.js' %}

{% for iter in ncjsam_entities %}

/* {{ iter.class_name }} */
{% include iter.template_file %}

{% endfor %}

/* Assets manager */

const kAssetsToPreload = [
{% for asset in ncjsam_assets %}
    '{{asset}}',
{% endfor %}
];

const kPending = 1;
const kSucceeded = 2;
const kFailed = 3;

export class AssetsManager {
    constructor(successCallback) {
        this._store = {};
        this._gltfLoader = new GLTFLoader();
        this._textureLoader = new THREE.TextureLoader();
        this._loadingState = kPending;

        const assetsManager = THREE.DefaultLoadingManager;
        assetsManager.onStart = () => {
            console.log("Assets loading started");
        };
        assetsManager.onLoad = () => {
            console.log("Assets loading done");
            if (this._loadingState == kFailed) {
                console.log("application loading failed!");
            } else {
                this._loadingState = kSucceeded;
                successCallback();
            }
        };
        assetsManager.onError = (url) => {
            console.log(`loading of "${url}" is failed`);
            this._loadingState = kFailed;
        };
    }

    start = () => {
        console.log('start AssetsManager');
        const scope = this;
        if (kAssetsToPreload.length > 0)
        {
            for(const assetId in kAssetsToPreload) {
                const url = kAssetsToPreload[assetId];
                const extension = url.split('.').pop().toLowerCase()
                var loader = null;

                if (extension == 'glb' || extension == 'gltf') {
                    loader = this._gltfLoader;
                } else if (extension == 'png' || extension == 'jpg' || extension == 'jpeg') {
                    loader = this._textureLoader;
                } else {
                    throw Error(`unknown asset type, url = '${url}', extension = '${extension}'`)
                }

                loader.load(
                    url,
                    (loadedAsset) => { scope._store[url] = loadedAsset; },
                    (xhr) => { console.log(`loading ${url}: ${xhr.loaded/xhr.total*100}`); },
                    (error) => { console.log(`an error occured while loading ${url}: ${error}`); },
                );

            }
        } else {
            const assetsManager = THREE.DefaultLoadingManager;
            assetsManager.onLoad();
        }
    }

    getLoadingManager = () => { return THREE.DefaultLoadingManager; }

    getAsset = (id) => { return this._store[id]; }
}

{% if ncjsam_daemon_context is defined %}
/* Reload manager */

class ReloadManager {
    constructor(main, state_id) {
        const scope = this;

        this._polling_interval = 1000;
        this._current_revision = null;
        this._main = main;
        this._state_id = state_id;

        this._code_revision_poller = new XMLHttpRequest();
        this._code_revision_poller.onload = (e) => {
            if (e.target.status == 200) {
                const response = JSON.parse(e.target.responseText);
                if (scope._current_revision != null && scope._current_revision != response.revision) {
                    scope.reload();
                }
                if (scope._current_revision == null) {
                    console.log(`initial version ${response.revision}`);
                }
                scope._current_revision = response.revision;
                scope._polling_interval = response.polling_interval;
            } else {
                console.warn(`failed to poll code revision: ${e.target.status}`)
            }

            setTimeout(() => { scope.poll(); },
                       scope._polling_interval);
        };

        this.poll();
    }

    poll = () => {
        this._code_revision_poller.open(
            'GET', '{{ ncjsam_daemon_context['endpoint'] }}/__ncjsam__/code-revision', true);
        this._code_revision_poller.send();
    }

    reload = () => {
        // create a state dump
        console.log('reloading page');
        const state = this._main.dump();

        // store the state
        const save_request = new XMLHttpRequest();
        save_request.open(
            'POST', `{{ ncjsam_daemon_context['endpoint'] }}/__ncjsam__/states/${this._state_id}`, false);
        save_request.setRequestHeader('Content-Type', 'application/json');
        save_request.send(JSON.stringify(
            {
                'contents': state,
            }
        ));

        // call for rebuild
        const rebuild_request = new XMLHttpRequest();
        rebuild_request.open(
            'POST', `{{ ncjsam_daemon_context['endpoint'] }}/__ncjsam__/rebuild-prefix`, false);
        rebuild_request.setRequestHeader('Content-Type', 'application/json');
        rebuild_request.send(JSON.stringify({}))

        // reload the window
        window.location.replace(
            `{{ ncjsam_daemon_context['endpoint'] }}/?state_id=${encodeURIComponent(this._state_id)}`
        );
    }

    maybe_restore_state = () => {
        const request = new XMLHttpRequest();
        request.open(
            'GET', `{{ ncjsam_daemon_context['endpoint'] }}/__ncjsam__/states/${this._state_id}`, false);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send();
        if (request.status == 200) {
            const response = JSON.parse(request.responseText);
            this._main.restore(response.contents);
        }
    }
}

{% endif %}

/* Main class */

export class Main {
    constructor() {
        // common initializations
        this._assetsManager = null;
        this._clock = new THREE.Clock();
        this._wallclock = 0;
        this._renderer = new THREE.WebGLRenderer();
        this._renderer.setSize(window.innerWidth, window.innerHeight);
        this._css2renderer = new CSS2DRenderer();
        this._css2renderer.setSize(window.innerWidth, window.innerHeight);
        this._css2renderer.domElement.style.position = 'absolute';
        this._css2renderer.domElement.style.top = '0px';
        this._css2renderer.domElement.style.pointerEvents = 'none';
        this._css3renderer = new CSS3DRenderer();
        this._css3renderer.setSize(window.innerWidth, window.innerHeight);
        this._css3renderer.domElement.style.position = 'absolute';
        this._css3renderer.domElement.style.top = '0px';
        this._css3renderer.domElement.style.pointerEvents = 'none';
        this._camera = null;
        this._scene = new THREE.Scene();
        this._controls = null;
        this._rootEntities = null;
        this._lastDt = null;
        this._eventQueue = [];
        this._subscribedEvents = new Set();
        this._pointerRaycaster = new THREE.Raycaster();
        this._pointerRaycasterPointer = new THREE.Vector2();
        this._pointerRaycasterIntersections = null;

        const url = new URL(window.location.href);
        const query = new URLSearchParams(url.search);
        this._state_id = query.has('state_id') ? query.get('state_id')
                                               : self.crypto.randomUUID();
        console.log(`state_id = ${this._state_id}`)

        this._guiLayer = document.createElement('div');
        this._guiLayer.style.background = 'rgba(0, 0, 0, 0)';
        this._guiLayer.style.border = '0px';
        this._guiLayer.style.width = '100%';
        this._guiLayer.style.height = '100%';
        this._guiLayer.style.position = 'absolute';
        this._guiLayer.style.userSelect = 'none';
        this._guiLayer.style.pointerEvents = 'none';
        this._guiLayer.setAttribute('draggable', false);

        document.body.appendChild(this._guiLayer);
        document.body.appendChild(this._renderer.domElement);
        document.body.appendChild(this._css2renderer.domElement);
        document.body.appendChild(this._css3renderer.domElement);
        
        addEventListener('resize', this.resize);
        addEventListener('pointermove', this.updatePointer);
    }

    init = (assetsManager) => {
        console.log('init Main');
        $.__setMain(this);

        // store items
        this._assetsManager = assetsManager;

        // create entities
        this._rootEntities = [
        {% for i in ncjsam_root_entities %}
            new {{ ncjsam_entities[i].class_name }}(
                '{{ ncjsam_entities[i].id }}', '{{ ncjsam_entities[i].path.as_string() }}',
                this._assetsManager, null),
        {% endfor %}
        ];
        this.registerEntities($);

        // init entities
        for(var i in this._rootEntities) {
            this._rootEntities[i].onEmerge(this._scene, this._guiLayer);
        }

        for(var i in this._rootEntities) {
            for(const kind of this._rootEntities[i].getSubscribedEvents()) {
                this._subscribedEvents.add(kind);
            }
        }

        // maybe reload state
        {% if ncjsam_daemon_context is defined %}
        this._reloadManager = new ReloadManager(this, this._state_id);
        this._reloadManager.maybe_restore_state();
        {% endif %}

        // init event queue
        this._eventQueue = [{
            'kind': 'ncjsam-init',
            'args': {},
        }];
        this.renewSystemSubscriptions();
    }

    renewSystemSubscriptions = () => {
        const systemEvents = new Set([
            'keydown', 'keyup',
            'pointercancel', 'pointerdown', 'pointermove', 'pointerup',
            'touchcancel', 'touchend', 'touchmove', 'touchstart',
            'wheel',
            'dblclick',
            'resize',
            'load', 'DOMContentLoaded',
        ])
        for(const kind of this._subscribedEvents) {
            if (systemEvents.has(kind)) {
                addEventListener(kind, (event) => {
                    this.enqueue(event.type, event);
                });
            }
        }
    }

    getCamera = () => { return this._camera; }

    getRenderer = () => { return this._renderer; }

    getPointerIntersections = () => {
        // TODO: maybe just guarantee a presence of a camera?
        if (!this._pointerRaycasterIntersections && this._camera) {
            this._pointerRaycaster.setFromCamera(this._pointerRaycasterPointer,
                                                 this._camera);
            this._pointerRaycasterIntersections = (
                this._pointerRaycaster.intersectObjects(this._scene.children));
        }
        return this._pointerRaycasterIntersections;
    }

    updatePointer = (event) => {
        this._pointerRaycasterPointer.x =  (event.clientX / window.innerWidth) * 2 - 1;
        this._pointerRaycasterPointer.y = -(event.clientY / window.innerHeight) * 2 + 1;
    }

    resize = (event) => {
        if (this._camera) {
            // TODO: this duplicates update inside the Camera Entity
            this._camera.aspect = window.innerWidth / window.innerHeight;
            this._camera.updateProjectionMatrix();
        }
        this._renderer.setSize(window.innerWidth, window.innerHeight);
        this._css2renderer.setSize(window.innerWidth, window.innerHeight);
        this._css3renderer.setSize(window.innerWidth, window.innerHeight);
        for(var i in this._rootEntities) {
            this._rootEntities[i].onResize(window.innerWidth,
                                           window.innerHeight);
        }
    }

    enqueue = (kind, args) => {
        this._eventQueue.push({'kind': kind, 'args': args});
    }

    advance = () => {
        // update state
        this._lastDt = this._clock.getDelta(); // seconds
        this._wallclock += this._lastDt;
        this._pointerRaycasterIntersections = null;

        // process events
        if (this._eventQueue.length > 0) {
            for(var event_index in this._eventQueue) {
                const event = this._eventQueue[event_index];
                for(var entity_index in this._rootEntities) {
                    this._rootEntities[entity_index].onEventPosted(event.kind,
                                                                   event.args);
                }
            }
            this._eventQueue = [];
        }

        // update camera
        var camera = null;
        for(var i in this._rootEntities) {
            this._rootEntities[i].onStep(false);
            if (!camera) {
                camera = this._rootEntities[i].query('camera', null);
            }
        }
        this._camera = camera; // TODO: don't update everytime

        // update controls
        if (this._controls) {
            this._controls.update();
        }

        // update physics step
        if (this._physicsWorld) {
            this._physicsWorld.stepSimulation(this._lastDt, 10);
        }

        // render a frame
        if (this._scene && this._camera) {
            this._renderer.render(this._scene, this._camera);
            this._css2renderer.render(this._scene, this._camera);
            this._css3renderer.render(this._scene, this._camera);
        } else {
            console.warn('not rendering due to abscence scene and/or camera, scene = ',
                         this._scene, ', camera = ', this._camera);
        }
    }

    getWallclock = () => { return this._wallclock; }
    getLastDt = () => { return this._lastDt; }
    registerEntities = (destination_object) => {
        for (var i in this._rootEntities) {
            this._rootEntities[i].registerEntity(destination_object);
        }
    }

    rootEntity = (key) => {
        // TODO: use dict instead list
        for(var i in this._rootEntities) {
            if (this._rootEntities[i].getFullPath() == key) {
                return this._rootEntities[i];
            }
        }
        return null;
    }

    dump = () => {
        const rootEntities = {};
        for (var i in this._rootEntities) {
            const entity = this._rootEntities[i];
            rootEntities[entity.getFullPath()] = entity.dump();
        }

        return {
            'ncjsam-dump': '0.1',
            'wallclock': this._wallclock,
            'last-dt': this._lastDt,
            'event-queue': this._eventQueue,
            'root-entities': rootEntities,
        }
    }

    restore = (state) => {
        console.log('state to restore', state);

        if (state['ncjsam-dump'] != '0.1') {
            throw Error(`unexpected dump version: "${state['ncjsam-dump']}"`)
        }

        this._wallclock = state['wallclock'];
        this._lastDt = state['last-dt'];
        this._eventQueue = state['event-queue'];
        for(var key in state['root-entities']) {
            const entityState = state['root-entities'][key];
            this.rootEntity(key).restore(entityState);
        }

        for(var i in this._rootEntities) {
            this._rootEntities[i].onStep(true);
        }
    }
}
