import { useGLTF, Center, Bounds, useBounds } from '@react-three/drei'

function Model({ url }) {
  const { scene } = useGLTF(url)
  const bounds = useBounds()

  scene.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true
      child.receiveShadow = true
    }
  })

  return (
    <primitive
      object={scene}
      onAfterRender={() => bounds.refresh().clip().fit()}
    />
  )
}

function BuildingModel({ url }) {
  return (
    <Bounds fit clip observe margin={1.2}>
      <Center>
        <Model url={url} />
      </Center>
    </Bounds>
  )
}

export default BuildingModel
