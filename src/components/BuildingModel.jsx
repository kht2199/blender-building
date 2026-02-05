import { useEffect, useMemo } from 'react'
import { useLoader, useThree } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import * as THREE from 'three'

function BuildingModel({ url }) {
  const gltf = useLoader(GLTFLoader, url)
  const { camera, controls } = useThree()

  const scene = useMemo(() => {
    const cloned = gltf.scene.clone()

    cloned.traverse((child) => {
      if (child.isMesh) {
        child.castShadow = true
        child.receiveShadow = true
      }
    })

    // Center the model
    const box = new THREE.Box3().setFromObject(cloned)
    const center = box.getCenter(new THREE.Vector3())

    cloned.position.x = -center.x
    cloned.position.z = -center.z

    return cloned
  }, [gltf])

  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene)
    const size = box.getSize(new THREE.Vector3())
    const maxDim = Math.max(size.x, size.y, size.z)
    const cameraDistance = maxDim * 1.5

    camera.position.set(cameraDistance, cameraDistance * 0.7, cameraDistance)

    if (controls) {
      controls.target.set(0, size.y / 2, 0)
      controls.update()
    }
  }, [scene, camera, controls])

  return <primitive object={scene} />
}

export default BuildingModel
