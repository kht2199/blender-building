"""건물 관련 함수들"""

import bpy
import math
from .utils import create_material


def create_floor(width, depth, height, floor_num, materials):
    """단일 층 생성"""
    slab_thickness = 0.2
    wall_thickness = 0.15

    floor_objects = []
    floor_base_z = (floor_num - 1) * height

    # 바닥 슬래브
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, floor_base_z + slab_thickness/2)
    )
    floor_slab = bpy.context.active_object
    floor_slab.name = f"Floor_{floor_num}_Slab"
    floor_slab.scale = (width, depth, slab_thickness)
    floor_slab.data.materials.append(materials['concrete'])
    floor_objects.append(floor_slab)

    # 벽 생성 (4면)
    wall_height = height - slab_thickness
    wall_positions = [
        ((0, depth/2 - wall_thickness/2, floor_base_z + slab_thickness + wall_height/2),
         (width, wall_thickness, wall_height), "Back"),
        ((0, -depth/2 + wall_thickness/2, floor_base_z + slab_thickness + wall_height/2),
         (width, wall_thickness, wall_height), "Front"),
        ((width/2 - wall_thickness/2, 0, floor_base_z + slab_thickness + wall_height/2),
         (wall_thickness, depth - wall_thickness*2, wall_height), "Right"),
        ((-width/2 + wall_thickness/2, 0, floor_base_z + slab_thickness + wall_height/2),
         (wall_thickness, depth - wall_thickness*2, wall_height), "Left"),
    ]

    for pos, scale, name in wall_positions:
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        wall = bpy.context.active_object
        wall.name = f"Floor_{floor_num}_Wall_{name}"
        wall.scale = scale
        wall.data.materials.append(materials['wall'])
        floor_objects.append(wall)

    # 창문 생성
    window_width = 1.2
    window_height = 1.5
    window_depth = wall_thickness + 0.02
    num_windows = max(1, int(width / 3))

    for i in range(num_windows):
        window_x = -width/2 + width/(num_windows+1) * (i+1)
        window_z = floor_base_z + slab_thickness + wall_height/2

        # 앞면 창문
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(window_x, -depth/2 + wall_thickness/2, window_z)
        )
        window = bpy.context.active_object
        window.name = f"Floor_{floor_num}_Window_Front_{i}"
        window.scale = (window_width, window_depth, window_height)
        window.data.materials.append(materials['glass'])
        floor_objects.append(window)

        # 뒷면 창문
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(window_x, depth/2 - wall_thickness/2, window_z)
        )
        window = bpy.context.active_object
        window.name = f"Floor_{floor_num}_Window_Back_{i}"
        window.scale = (window_width, window_depth, window_height)
        window.data.materials.append(materials['glass'])
        floor_objects.append(window)

    return floor_objects


def create_building(name, width=8, depth=6, floor_height=3.5, num_floors=2,
                   wall_color=(0.85, 0.82, 0.78, 1.0)):
    """건물 생성"""
    materials = {
        'concrete': create_material(f"{name}_Concrete", (0.5, 0.5, 0.5, 1.0), roughness=0.9),
        'wall': create_material(f"{name}_Wall", wall_color, roughness=0.7),
        'glass': create_material(f"{name}_Glass", (0.6, 0.8, 0.9, 0.5), metallic=0.9, roughness=0.1),
        'roof': create_material(f"{name}_Roof", (0.3, 0.3, 0.35, 1.0), roughness=0.8),
    }

    building_objects = []

    for floor_num in range(1, num_floors + 1):
        floor_objects = create_floor(width, depth, floor_height, floor_num, materials)
        building_objects.extend(floor_objects)

    # 지붕 생성
    roof_z = num_floors * floor_height + 0.15
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, roof_z))
    roof = bpy.context.active_object
    roof.name = f"{name}_Roof"
    roof.scale = (width + 0.3, depth + 0.3, 0.3)
    roof.data.materials.append(materials['roof'])
    building_objects.append(roof)

    # 부모 오브젝트
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = name

    for obj in building_objects:
        obj.parent = parent

    return parent


def create_text_on_roof_edge(text, building, width, depth, num_floors, floor_height,
                             text_color=(0.1, 0.1, 0.1, 1.0), text_size=1.0):
    """건물 지붕 가장자리에 텍스트 추가"""
    bpy.ops.object.text_add()
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = text_size
    text_obj.data.extrude = 0.08
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'BOTTOM'

    bpy.ops.object.convert(target='MESH')

    mat = create_material(f"{building.name}_RoofText_{text}", text_color, roughness=0.3)
    text_obj.data.materials.append(mat)

    roof_z = num_floors * floor_height + 0.3
    text_obj.location = (0, -depth/2 - 0.15, roof_z)
    text_obj.rotation_euler = (math.pi/2, 0, 0)

    text_obj.name = f"{building.name}_RoofText_{text}"
    text_obj.parent = building

    return text_obj


def create_text_on_wall(text, building, floor_num=1, wall_side="front",
                        text_color=(0.1, 0.1, 0.1, 1.0)):
    """건물 벽면에 텍스트 추가"""
    bpy.ops.object.text_add()
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = 0.8
    text_obj.data.extrude = 0.05
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    bpy.ops.object.convert(target='MESH')

    mat = create_material(f"{building.name}_Text_{text}", text_color, roughness=0.3)
    text_obj.data.materials.append(mat)

    floor_height = 3.5
    depth = 6
    text_z = (floor_num - 1) * floor_height + floor_height * 0.6

    if wall_side == "front":
        text_obj.location = (0, -depth/2 - 0.01, text_z)
        text_obj.rotation_euler = (math.pi/2, 0, 0)
    elif wall_side == "back":
        text_obj.location = (0, depth/2 + 0.01, text_z)
        text_obj.rotation_euler = (math.pi/2, 0, math.pi)
    elif wall_side == "left":
        text_obj.location = (-depth/2 - 0.01, 0, text_z)
        text_obj.rotation_euler = (math.pi/2, 0, -math.pi/2)
    elif wall_side == "right":
        text_obj.location = (depth/2 + 0.01, 0, text_z)
        text_obj.rotation_euler = (math.pi/2, 0, math.pi/2)

    text_obj.name = f"{building.name}_Text_{text}"
    text_obj.parent = building

    return text_obj


def create_entrance(building, width=2, height=2.5, depth=6):
    """건물 입구 생성"""
    frame_mat = create_material(f"{building.name}_EntranceFrame",
                                (0.2, 0.2, 0.25, 1.0), metallic=0.8)
    door_mat = create_material(f"{building.name}_Door",
                              (0.4, 0.25, 0.15, 1.0), roughness=0.6)

    entrance_objects = []
    frame_thickness = 0.1
    frame_depth = 0.15

    # 상단 프레임
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth/2 + frame_depth/2, height))
    top_frame = bpy.context.active_object
    top_frame.name = f"{building.name}_Entrance_TopFrame"
    top_frame.scale = (width + frame_thickness*2, frame_depth, frame_thickness)
    top_frame.data.materials.append(frame_mat)
    top_frame.parent = building
    entrance_objects.append(top_frame)

    # 좌측 프레임
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-width/2 - frame_thickness/2, -depth/2 + frame_depth/2, height/2)
    )
    left_frame = bpy.context.active_object
    left_frame.name = f"{building.name}_Entrance_LeftFrame"
    left_frame.scale = (frame_thickness, frame_depth, height)
    left_frame.data.materials.append(frame_mat)
    left_frame.parent = building
    entrance_objects.append(left_frame)

    # 우측 프레임
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(width/2 + frame_thickness/2, -depth/2 + frame_depth/2, height/2)
    )
    right_frame = bpy.context.active_object
    right_frame.name = f"{building.name}_Entrance_RightFrame"
    right_frame.scale = (frame_thickness, frame_depth, height)
    right_frame.data.materials.append(frame_mat)
    right_frame.parent = building
    entrance_objects.append(right_frame)

    # 문
    door_width = (width - 0.1) / 2
    for i, x_offset in enumerate([-door_width/2 - 0.025, door_width/2 + 0.025]):
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_offset, -depth/2 + frame_depth/2, height/2 - 0.1)
        )
        door = bpy.context.active_object
        door.name = f"{building.name}_Door_{i}"
        door.scale = (door_width, 0.05, height - 0.3)
        door.data.materials.append(door_mat)
        door.parent = building
        entrance_objects.append(door)

    # 캐노피
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth/2 - 0.5, height + 0.2))
    canopy = bpy.context.active_object
    canopy.name = f"{building.name}_Canopy"
    canopy.scale = (width + 1, 1.2, 0.1)
    canopy.data.materials.append(frame_mat)
    canopy.parent = building
    entrance_objects.append(canopy)

    return entrance_objects
