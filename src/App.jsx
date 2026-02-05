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
    ground: '#669900',
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

function Moon() {
  return (
    <group position={[60, 80, -80]}>
      {/* 달 구체 */}
      <mesh>
        <sphereGeometry args={[8, 32, 32]} />
        <meshStandardMaterial
          color="#fffff8"
          emissive="#ffffee"
          emissiveIntensity={2}
          roughness={0.5}
        />
      </mesh>
      {/* 달빛 조명 */}
      <directionalLight
        position={[0, 0, 0]}
        intensity={0.8}
        color="#ccddef"
        castShadow
        shadow-mapSize={[1024, 1024]}
        shadow-camera-far={200}
        shadow-camera-left={-100}
        shadow-camera-right={100}
        shadow-camera-top={100}
        shadow-camera-bottom={-100}
      />
    </group>
  )
}

function StreetLight({ position, color = "#ffaa55" }) {
  return (
    <group position={position}>
      {/* 기둥 */}
      <mesh position={[0, 4, 0]}>
        <cylinderGeometry args={[0.1, 0.15, 8, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.8} roughness={0.3} />
      </mesh>
      {/* 조명 헤드 */}
      <mesh position={[0, 8.2, 0]}>
        <boxGeometry args={[1, 0.4, 0.5]} />
        <meshStandardMaterial color="#444444" metalness={0.5} />
      </mesh>
      {/* 전구 */}
      <mesh position={[0, 7.9, 0]}>
        <sphereGeometry args={[0.2, 8, 8]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} />
      </mesh>
      {/* 포인트 라이트 */}
      <pointLight
        position={[0, 7.5, 0]}
        intensity={50}
        distance={40}
        color={color}
        decay={1.5}
      />
    </group>
  )
}

function StreetLights() {
  const positions = [
    // 도로 앞쪽 가로등
    { pos: [-40, -12], color: "#ffaa55" },
    { pos: [-25, -12], color: "#ffaa55" },
    { pos: [-10, -12], color: "#ffaa55" },
    { pos: [5, -12], color: "#ffaa55" },
    { pos: [20, -12], color: "#ffaa55" },
    { pos: [35, -12], color: "#ffaa55" },
    // 건물 뒤쪽 가로등
    { pos: [-35, 10], color: "#ffcc66" },
    { pos: [-15, 10], color: "#ffcc66" },
    { pos: [5, 10], color: "#ffcc66" },
    { pos: [25, 10], color: "#ffcc66" },
    { pos: [40, 10], color: "#ffcc66" },
    // 건물 옆쪽 가로등
    { pos: [-40, 0], color: "#ffdd88" },
    { pos: [45, 0], color: "#ffdd88" },
  ]
  return (
    <group>
      {positions.map((item, i) => (
        <StreetLight key={i} position={[item.pos[0], 0, item.pos[1]]} color={item.color} />
      ))}
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
              <Moon />
              <StreetLights />
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
