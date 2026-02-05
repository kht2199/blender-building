"""환경 요소 (나무, 도로 등)"""

import bpy
from .utils import create_material


def create_tree(location, height=4, name="Tree"):
    """나무 생성"""
    tree_objects = []

    trunk_mat = create_material(f"{name}_Trunk", (0.35, 0.2, 0.1, 1.0), roughness=0.9)
    trunk_radius = 0.15
    trunk_height = height * 0.4

    bpy.ops.mesh.primitive_cylinder_add(
        radius=trunk_radius,
        depth=trunk_height,
        location=(location[0], location[1], trunk_height/2)
    )
    trunk = bpy.context.active_object
    trunk.name = f"{name}_Trunk"
    trunk.data.materials.append(trunk_mat)
    tree_objects.append(trunk)

    leaf_mat = create_material(f"{name}_Leaves", (0.2, 0.5, 0.15, 1.0), roughness=0.8)
    leaf_positions = [
        (0, 0, trunk_height + height * 0.3),
        (0.3, 0.3, trunk_height + height * 0.15),
        (-0.3, 0.3, trunk_height + height * 0.15),
        (0.3, -0.3, trunk_height + height * 0.15),
        (-0.3, -0.3, trunk_height + height * 0.15),
    ]

    for i, pos in enumerate(leaf_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=height * 0.25,
            location=(location[0] + pos[0], location[1] + pos[1], pos[2])
        )
        leaf = bpy.context.active_object
        leaf.name = f"{name}_Leaves_{i}"
        leaf.data.materials.append(leaf_mat)
        tree_objects.append(leaf)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent = bpy.context.active_object
    parent.name = name

    for obj in tree_objects:
        obj.parent = parent

    return parent


def create_road(length=30, width=6, location=(0, -15, 0)):
    """도로 생성"""
    road_objects = []

    asphalt_mat = create_material("Asphalt", (0.15, 0.15, 0.15, 1.0), roughness=0.95)
    line_mat = create_material("RoadLine", (0.95, 0.95, 0.9, 1.0), roughness=0.5)

    # 도로 표면
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0], location[1], location[2] - 0.05)
    )
    road = bpy.context.active_object
    road.name = "Road_Surface"
    road.scale = (length, width, 0.1)
    road.data.materials.append(asphalt_mat)
    road_objects.append(road)

    # 중앙선
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(location[0], location[1], location[2] + 0.01)
    )
    center_line = bpy.context.active_object
    center_line.name = "Road_CenterLine"
    center_line.scale = (length, 0.15, 0.02)
    center_line.data.materials.append(line_mat)
    road_objects.append(center_line)

    # 차선 (점선)
    dash_length = 2
    gap_length = 1
    num_dashes = int(length / (dash_length + gap_length))

    for i in range(num_dashes):
        x_pos = -length/2 + (dash_length + gap_length) * i + dash_length/2 + 1
        for y_offset in [-width/4, width/4]:
            bpy.ops.mesh.primitive_cube_add(
                size=1,
                location=(x_pos, location[1] + y_offset, location[2] + 0.01)
            )
            dash = bpy.context.active_object
            dash.name = f"Road_Dash_{i}_{y_offset}"
            dash.scale = (dash_length, 0.1, 0.02)
            dash.data.materials.append(line_mat)
            road_objects.append(dash)

    # 인도
    sidewalk_mat = create_material("Sidewalk", (0.6, 0.6, 0.6, 1.0), roughness=0.85)
    for y_offset in [-width/2 - 1, width/2 + 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(location[0], location[1] + y_offset, location[2] + 0.05)
        )
        sidewalk = bpy.context.active_object
        sidewalk.name = f"Sidewalk_{y_offset}"
        sidewalk.scale = (length, 2, 0.2)
        sidewalk.data.materials.append(sidewalk_mat)
        road_objects.append(sidewalk)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent = bpy.context.active_object
    parent.name = "Road"

    for obj in road_objects:
        obj.parent = parent

    return parent
