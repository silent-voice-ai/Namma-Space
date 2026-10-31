import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';

// 1. Scene & Main Perspective Camera Setup
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x050505);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 2, 5);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
container.appendChild(renderer.domElement);

// 2. Orbit Controls for Navigation
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// 3. Lighting & Reference Grid
scene.add(new THREE.AmbientLight(0xffffff, 1.2));
const gridHelper = new THREE.GridHelper(10, 10, 0x00ffcc, 0x333333);
gridHelper.position.y = -1;
scene.add(gridHelper);

// 4. Load Scanned Point Cloud Asset (points3D.ply from COLMAP output)
const loader = new PLYLoader();
loader.load('./points3D.ply', (geometry) => {
    geometry.computeVertexNormals();
    const material = new THREE.PointsMaterial({
        size: 0.04,
        vertexColors: true
    });
    const pointCloud = new THREE.Points(geometry, material);
    
    // Rotate and position model if required by COLMAP coordinates
    pointCloud.rotation.x = -Math.PI / 2;
    scene.add(pointCloud);
    
    document.getElementById('sys-status').innerText = 'ONLINE (MODEL LOADED)';
}, 
(xhr) => {
    if (xhr.total > 0) {
        const percent = Math.round((xhr.loaded / xhr.total) * 100);
        document.getElementById('sys-status').innerText = `LOADING MODEL: ${percent}%`;
    }
}, 
(error) => {
    console.warn('points3D.ply not found locally. Displaying fallback grid/scene.', error);
    document.getElementById('sys-status').innerText = 'ONLINE (FALLBACK VIEW)';
});

// 5. Minimap Orthographic Camera Setup
const miniCamera = new THREE.OrthographicCamera(-4, 4, 4, -4, 0.1, 100);
miniCamera.position.set(0, 10, 0);
miniCamera.lookAt(0, 0, 0);

// 6. Responsive Window Resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// 7. Main Render & Animation Loop
function animate() {
    requestAnimationFrame(animate);
    
    controls.update();

    // Render Main Perspective Viewport
    renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.setScissor(0, 0, window.innerWidth, window.innerHeight);
    renderer.setScissorTest(false);
    renderer.render(scene, camera);

    // Render Minimap Viewport (Top-Right Overlay)
    const mWidth = 150;
    const mHeight = 150;
    const mLeft = window.innerWidth - mWidth - 20;
    const mBottom = window.innerHeight - mHeight - 40;

    renderer.setViewport(mLeft, mBottom, mWidth, mHeight);
    renderer.setScissor(mLeft, mBottom, mWidth, mHeight);
    renderer.setScissorTest(true);
    
    // Make minimap camera track main camera's X/Z position overhead
    miniCamera.position.x = camera.position.x;
    miniCamera.position.z = camera.position.z;
    miniCamera.lookAt(camera.position.x, 0, camera.position.z);

    renderer.render(scene, miniCamera);
}

animate();
console.log("Namma Space 3DGS Web Viewer initialized successfully.");