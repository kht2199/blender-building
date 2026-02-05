import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, ContactShadows, Grid, Sky } from '@react-three/drei'
import BuildingModel from './components/BuildingModel'
import './App.css'

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
  return (
    <div className="app">
      <main className="canvas-container full-width">
        <Canvas
          shadows
          camera={{ position: [40, 30, 40], fov: 60 }}
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
            <BuildingModel url="/output/combined_scene.gltf" />
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
            minDistance={10}
            maxDistance={150}
            minPolarAngle={Math.PI / 3}
            maxPolarAngle={Math.PI / 3}
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
          <h3>Combined Scene</h3>
          <p>Office, Shop, Modern buildings with road and trees</p>
        </div>
      </main>
    </div>
  )
}

export default App
