import { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, ContactShadows, Grid, Sky } from '@react-three/drei'
import BuildingModel from './components/BuildingModel'
import './App.css'

const themes = {
  dark: {
    background: '#1a1a2e',
    ground: '#3a5a40',
    gridColor: '#0f3460',
    ambientIntensity: 0.4,
    skyPosition: [100, 50, 100],
    hemisphereSky: '#87ceeb',
    hemisphereGround: '#4a6741',
  },
  light: {
    background: '#e8f4f8',
    ground: '#90be6d',
    gridColor: '#aaccdd',
    ambientIntensity: 0.7,
    skyPosition: [100, 80, 100],
    hemisphereSky: '#ffffff',
    hemisphereGround: '#90be6d',
  }
}

function LoadingFallback() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#e94560" wireframe />
    </mesh>
  )
}

function Ground({ color }) {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
      <planeGeometry args={[200, 200]} />
      <meshStandardMaterial color={color} roughness={0.9} />
    </mesh>
  )
}

function App() {
  const [isDark, setIsDark] = useState(true)
  const theme = isDark ? themes.dark : themes.light

  return (
    <div className={`app ${isDark ? 'dark' : 'light'}`}>
      <main className="canvas-container full-width">
        <Canvas
          shadows
          camera={{ position: [40, 30, 40], fov: 60 }}
          gl={{ antialias: true }}
        >
          <color attach="background" args={[theme.background]} />

          <ambientLight intensity={theme.ambientIntensity} />
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
          <hemisphereLight args={[theme.hemisphereSky, theme.hemisphereGround, 0.3]} />

          <Suspense fallback={<LoadingFallback />}>
            <BuildingModel url="/output/combined_scene.gltf" />
          </Suspense>

          <Ground color={theme.ground} />
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
            cellColor={theme.gridColor}
            sectionSize={5}
            sectionThickness={1}
            sectionColor={theme.gridColor}
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
          <Sky sunPosition={theme.skyPosition} />
        </Canvas>

        <button className="theme-toggle" onClick={() => setIsDark(!isDark)}>
          {isDark ? '☀️ Light' : '🌙 Dark'}
        </button>

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
