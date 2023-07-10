#!/bin/bash

THREE_VER='0.150.1'
wget -O ./ncjsam/compiler/templates/three.module.js https://unpkg.com/three@${THREE_VER}/build/three.module.js
wget -O ./ncjsam/compiler/templates/GLTFLoader.js https://unpkg.com/three@${THREE_VER}/examples/jsm/loaders/GLTFLoader.js
wget -O ./ncjsam/compiler/templates/BufferGeometryUtils.js https://unpkg.com/three@${THREE_VER}/examples/jsm/utils/BufferGeometryUtils.js
wget -O ./ncjsam/compiler/templates/OrbitControls.js https://unpkg.com/three@${THREE_VER}/examples/jsm/controls/OrbitControls.js
wget -O ./ncjsam/compiler/templates/CSS2DRenderer.js https://unpkg.com/three@${THREE_VER}/examples/jsm/renderers/CSS2DRenderer.js
wget -O ./ncjsam/compiler/templates/CSS3DRenderer.js https://unpkg.com/three@${THREE_VER}/examples/jsm/renderers/CSS3DRenderer.js


touch ./ncjsam/compiler/templates/three.module.js
touch ./ncjsam/compiler/templates/GLTFLoader.js
touch ./ncjsam/compiler/templates/BufferGeometryUtils.js
touch ./ncjsam/compiler/templates/OrbitControls.js
touch ./ncjsam/compiler/templates/CSS2DRenderer.js
touch ./ncjsam/compiler/templates/CSS3DRenderer.js


sed -i "s/\.\.\/utils\//\//" ./ncjsam/compiler/templates/GLTFLoader.js
