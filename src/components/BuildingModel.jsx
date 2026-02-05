import { useMemo } from 'react'
import { useGLTF, Center, Bounds } from '@react-three/drei'

function Model({ url }) {
  const { scene } = useGLTF(url)

  const clonedScene = useMemo(() => {
    const cloned = scene.clone(true)
    cloned.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })
    return cloned
  }, [scene])

  return <primitive object={clonedScene} />
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
