"""유틸리티 함수들"""

import bpy
import os

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def clear_scene():
    """씬의 모든 오브젝트 삭제"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)


def create_material(name, color, metallic=0.0, roughness=0.5, alpha=1.0):
    """머티리얼 생성

    Args:
        alpha: 투명도 (0.0=완전 투명, 1.0=불투명)
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    # 투명도 설정
    if alpha < 1.0:
        bsdf.inputs['Alpha'].default_value = alpha
        mat.blend_method = 'BLEND'
        mat.surface_render_method = 'BLENDED'

    return mat


def export_to_gltf(filepath, export_format='GLTF_SEPARATE'):
    """GLTF 형식으로 내보내기"""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=export_format,
        export_apply=True,
        export_materials='EXPORT'
    )
    print(f"Exported to: {filepath}")
