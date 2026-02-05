import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Building data
const buildings = [
  {
    id: 'building_basic',
    name: 'Basic Building',
    description: '2-story building with TEST text, entrance, and trees',
    file: '/output/building_basic.gltf'
  },
  {
    id: 'office_building',
    name: 'Office Building',
    description: '3-story office with OFFICE text, road, and trees',
    file: '/output/office_building.gltf'
  },
  {
    id: 'shop_building',
    name: 'Shop Building',
    description: '1-story shop with SHOP text and entrance',
    file: '/output/shop_building.gltf'
  },
  {
    id: 'city_block',
    name: 'City Block',
    description: 'Multiple buildings: apartment, office, cafe with road',
    file: '/output/city_block.gltf'
  },
  {
    id: 'modern_building',
    name: 'Modern Building',
    description: '3-story modern dark building with MODERN text',
    file: '/output/modern_building.gltf'
  }
];

// Three.js setup
let scene, camera, renderer, controls;
let currentModel = null;

function init() {
  // Scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x1a1a2e);

  // Camera
  camera = new THREE.PerspectiveCamera(
    60,
    (window.innerWidth - 280) / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(20, 15, 20);

  // Renderer
  const canvas = document.getElementById('three-canvas');
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(window.innerWidth - 280, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;

  // Controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = 5;
  controls.maxDistance = 100;
  controls.target.set(0, 3, 0);

  // Lighting
  setupLighting();

  // Ground
  createGround();

  // Grid helper
  const gridHelper = new THREE.GridHelper(100, 50, 0x0f3460, 0x0f3460);
  gridHelper.position.y = -0.01;
  scene.add(gridHelper);

  // Window resize handler
  window.addEventListener('resize', onWindowResize);

  // Start animation loop
  animate();

  // Setup UI
  setupBuildingList();

  // Load first building
  loadBuilding(buildings[0]);
}

function setupLighting() {
  // Ambient light
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);

  // Directional light (sun)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
  directionalLight.position.set(30, 50, 30);
  directionalLight.castShadow = true;
  directionalLight.shadow.mapSize.width = 2048;
  directionalLight.shadow.mapSize.height = 2048;
  directionalLight.shadow.camera.near = 0.5;
  directionalLight.shadow.camera.far = 150;
  directionalLight.shadow.camera.left = -50;
  directionalLight.shadow.camera.right = 50;
  directionalLight.shadow.camera.top = 50;
  directionalLight.shadow.camera.bottom = -50;
  scene.add(directionalLight);

  // Fill light
  const fillLight = new THREE.DirectionalLight(0x8ecae6, 0.5);
  fillLight.position.set(-20, 20, -20);
  scene.add(fillLight);

  // Hemisphere light for sky/ground color
  const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x4a6741, 0.3);
  scene.add(hemiLight);
}

function createGround() {
  const groundGeometry = new THREE.PlaneGeometry(200, 200);
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x3a5a40,
    roughness: 0.9
  });
  const ground = new THREE.Mesh(groundGeometry, groundMaterial);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);
}

function setupBuildingList() {
  const listContainer = document.getElementById('building-list');

  buildings.forEach((building, index) => {
    const item = document.createElement('li');
    item.className = 'building-item' + (index === 0 ? ' active' : '');
    item.dataset.id = building.id;
    item.innerHTML = `
      <h3>${building.name}</h3>
      <p>${building.description}</p>
    `;
    item.addEventListener('click', () => {
      document.querySelectorAll('.building-item').forEach(el => el.classList.remove('active'));
      item.classList.add('active');
      loadBuilding(building);
    });
    listContainer.appendChild(item);
  });
}

function loadBuilding(building) {
  const loadingEl = document.getElementById('loading');
  const infoName = document.getElementById('model-name');
  const infoDesc = document.getElementById('model-description');

  loadingEl.style.display = 'block';

  // Remove current model
  if (currentModel) {
    scene.remove(currentModel);
    currentModel.traverse((child) => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) {
          child.material.forEach(m => m.dispose());
        } else {
          child.material.dispose();
        }
      }
    });
  }

  // Load new model
  const loader = new GLTFLoader();
  loader.load(
    building.file,
    (gltf) => {
      currentModel = gltf.scene;

      // Enable shadows for all meshes
      currentModel.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true;
          child.receiveShadow = true;
        }
      });

      // Center the model
      const box = new THREE.Box3().setFromObject(currentModel);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());

      currentModel.position.x = -center.x;
      currentModel.position.z = -center.z;

      scene.add(currentModel);

      // Adjust camera
      const maxDim = Math.max(size.x, size.y, size.z);
      const cameraDistance = maxDim * 1.5;
      camera.position.set(cameraDistance, cameraDistance * 0.7, cameraDistance);
      controls.target.set(0, size.y / 2, 0);
      controls.update();

      // Update info
      infoName.textContent = building.name;
      infoDesc.textContent = building.description;

      loadingEl.style.display = 'none';
    },
    (progress) => {
      const percent = (progress.loaded / progress.total * 100).toFixed(0);
      loadingEl.querySelector('p').textContent = `Loading... ${percent}%`;
    },
    (error) => {
      console.error('Error loading model:', error);
      loadingEl.querySelector('p').textContent = 'Error loading model';
    }
  );
}

function onWindowResize() {
  const width = window.innerWidth - 280;
  const height = window.innerHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  renderer.setSize(width, height);
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// Start the application
init();
