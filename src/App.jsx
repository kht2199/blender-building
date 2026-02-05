import { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, ContactShadows, Grid, Sky } from '@react-three/drei'
import BuildingModel from './components/BuildingModel'
import Sidebar from './components/Sidebar'
import './App.css'

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
]

function LoadingFallback() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#e94560" wireframe />
    </mesh>
  )
}

function Ground() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
      <planeGeometry args={[200, 200]} />
      <meshStandardMaterial color="#3a5a40" roughness={0.9} />
    </mesh>
  )
}

function App() {
  const [selectedBuilding, setSelectedBuilding] = useState(buildings[0])

  return (
    <div className="app">
      <Sidebar
        buildings={buildings}
        selectedBuilding={selectedBuilding}
        onSelect={setSelectedBuilding}
      />
      <main className="canvas-container">
        <Canvas
          shadows
          camera={{ position: [20, 15, 20], fov: 60 }}
          gl={{ antialias: true }}
        >
          <color attach="background" args={['#1a1a2e']} />

          <ambientLight intensity={0.4} />
          <directionalLight
            position={[30, 50, 30]}
            intensity={1.2}
            castShadow
            shadow-mapSize={[2048, 2048]}
            shadow-camera-far={150}
            shadow-camera-left={-50}
            shadow-camera-right={50}
            shadow-camera-top={50}
            shadow-camera-bottom={-50}
          />
          <directionalLight position={[-20, 20, -20]} intensity={0.5} color="#8ecae6" />
          <hemisphereLight args={['#87ceeb', '#4a6741', 0.3]} />

          <Suspense fallback={<LoadingFallback />}>
            <BuildingModel key={selectedBuilding.id} url={selectedBuilding.file} />
          </Suspense>

          <Ground />
          <ContactShadows
            position={[0, 0, 0]}
            opacity={0.4}
            scale={100}
            blur={2}
            far={50}
          />
          <Grid
            args={[100, 100]}
            cellSize={1}
            cellThickness={0.5}
            cellColor="#0f3460"
            sectionSize={5}
            sectionThickness={1}
            sectionColor="#0f3460"
            fadeDistance={100}
            infiniteGrid
          />

          <OrbitControls
            enableDamping
            dampingFactor={0.05}
            minDistance={5}
            maxDistance={100}
            minPolarAngle={Math.PI / 6}
            maxPolarAngle={Math.PI / 6}
            target={[0, 3, 0]}
          />
          <Sky sunPosition={[100, 50, 100]} />
        </Canvas>

        <div className="controls">
          <p><kbd>Left Click + Drag</kbd> Rotate</p>
          <p><kbd>Right Click + Drag</kbd> Pan</p>
          <p><kbd>Scroll</kbd> Zoom</p>
        </div>

        <div className="info">
          <h3>{selectedBuilding.name}</h3>
          <p>{selectedBuilding.description}</p>
        </div>
      </main>
    </div>
  )
}

export default App
