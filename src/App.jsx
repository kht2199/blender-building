import { useState, Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, ContactShadows, Grid, Sky, Cloud, Stars } from '@react-three/drei'
import BuildingModel from './components/BuildingModel'
import './App.css'

const themes = {
  dark: {
    background: '#000000',
    ground: '#3a5a40',
    gridColor: '#0f3460',
    ambientIntensity: 0.1,
    hemisphereSky: '#0a0a15',
    hemisphereGround: '#1a2a1a',
  },
  light: {
    background: '#e8f4f8',
    ground: '#90be6d',
    gridColor: '#aaccdd',
    ambientIntensity: 0.7,
    skyPosition: [100, 80, 100],
    hemisphereSky: '#ffffff',
    hemisphereGround: '#90be6d',
    cloudColor: '#ffffff',
    cloudOpacity: 0.8,
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

function Clouds({ color, opacity }) {
  return (
    <group>
      <Cloud position={[-30, 25, -20]} speed={0.2} opacity={opacity} color={color} />
      <Cloud position={[30, 30, -30]} speed={0.1} opacity={opacity} color={color} />
      <Cloud position={[0, 28, -40]} speed={0.15} opacity={opacity} color={color} />
      <Cloud position={[-50, 32, 10]} speed={0.1} opacity={opacity} color={color} />
      <Cloud position={[50, 27, 20]} speed={0.2} opacity={opacity} color={color} />
    </group>
  )
}

function StreetLight({ position }) {
  return (
    <group position={position}>
      {/* 기둥 */}
      <mesh position={[0, 3, 0]}>
        <cylinderGeometry args={[0.1, 0.15, 6, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.8} roughness={0.3} />
      </mesh>
      {/* 조명 헤드 */}
      <mesh position={[0, 6.2, 0]}>
        <boxGeometry args={[0.8, 0.3, 0.4]} />
        <meshStandardMaterial color="#444444" metalness={0.5} />
      </mesh>
      {/* 포인트 라이트 */}
      <pointLight
        position={[0, 5.8, 0]}
        intensity={15}
        distance={20}
        color="#ffaa55"
        castShadow
      />
    </group>
  )
}

function StreetLights() {
  const positions = [
    [-35, -12], [-20, -12], [-5, -12], [10, -12], [25, -12], [40, -12],
  ]
  return (
    <group>
      {positions.map((pos, i) => (
        <StreetLight key={i} position={[pos[0], 0, pos[1]]} />
      ))}
    </group>
  )
}

function BuildingLights() {
  return (
    <group>
      {/* Office Building 조명 */}
      <pointLight position={[-25, 8, -6]} intensity={8} distance={15} color="#ffffcc" />
      <spotLight position={[-25, 0.5, -8]} angle={0.5} intensity={10} distance={12} color="#ffdd88" target-position={[-25, 0, -5]} />

      {/* Shop Building 조명 */}
      <pointLight position={[0, 5, -4]} intensity={10} distance={12} color="#ff6644" />
      <spotLight position={[0, 0.5, -5]} angle={0.6} intensity={8} distance={10} color="#ffaa66" />

      {/* Modern Building 조명 */}
      <pointLight position={[25, 8, -6]} intensity={8} distance={15} color="#aaccff" />
      <spotLight position={[25, 0.5, -8]} angle={0.5} intensity={10} distance={12} color="#88aaff" target-position={[25, 0, -5]} />
    </group>
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

          {!isDark && (
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
          )}

          {isDark && (
            <>
              {/* 달빛 효과 */}
              <directionalLight
                position={[-30, 40, -20]}
                intensity={0.15}
                color="#6688cc"
              />
              <StreetLights />
              <BuildingLights />
            </>
          )}

          <directionalLight position={[-20, 20, -20]} intensity={isDark ? 0.1 : 0.5} color="#8ecae6" />
          <hemisphereLight args={[theme.hemisphereSky, theme.hemisphereGround, isDark ? 0.1 : 0.3]} />

          <Suspense fallback={<LoadingFallback />}>
            <BuildingModel url="/output/combined_scene.gltf" />
          </Suspense>

          <Ground color={theme.ground} />
          <ContactShadows
            position={[0, 0, 0]}
            opacity={isDark ? 0.6 : 0.4}
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

          {!isDark && (
            <>
              <Sky sunPosition={theme.skyPosition} />
              <Clouds color={theme.cloudColor} opacity={theme.cloudOpacity} />
            </>
          )}
          {isDark && <Stars radius={100} depth={50} count={2000} factor={4} fade speed={1} />}
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
