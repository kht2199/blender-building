"""건물 관련 함수들"""

import bpy
import math
from .utils import create_material


def create_floor(width, depth, height, floor_num, materials, entrance_width=0):
    """단일 층 생성

    Args:
        entrance_width: 1층 입구 너비 (0이면 입구 없음)
    """
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

    # 벽 생성
    wall_height = height - slab_thickness

    # 뒷벽
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        0, depth/2 - wall_thickness/2, floor_base_z + slab_thickness + wall_height/2
    ))
    back_wall = bpy.context.active_object
    back_wall.name = f"Floor_{floor_num}_Wall_Back"
    back_wall.scale = (width, wall_thickness, wall_height)
    back_wall.data.materials.append(materials['wall'])
    floor_objects.append(back_wall)

    # 앞벽 - 1층이고 입구가 있으면 좌/우로 분리
    if floor_num == 1 and entrance_width > 0:
        # 입구 좌측 벽
        left_wall_width = (width - entrance_width) / 2
        if left_wall_width > 0:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(
                -width/2 + left_wall_width/2,
                -depth/2 + wall_thickness/2,
                floor_base_z + slab_thickness + wall_height/2
            ))
            left_front = bpy.context.active_object
            left_front.name = f"Floor_{floor_num}_Wall_Front_Left"
            left_front.scale = (left_wall_width, wall_thickness, wall_height)
            left_front.data.materials.append(materials['wall'])
            floor_objects.append(left_front)

        # 입구 우측 벽
        right_wall_width = (width - entrance_width) / 2
        if right_wall_width > 0:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(
                width/2 - right_wall_width/2,
                -depth/2 + wall_thickness/2,
                floor_base_z + slab_thickness + wall_height/2
            ))
            right_front = bpy.context.active_object
            right_front.name = f"Floor_{floor_num}_Wall_Front_Right"
            right_front.scale = (right_wall_width, wall_thickness, wall_height)
            right_front.data.materials.append(materials['wall'])
            floor_objects.append(right_front)
    else:
        # 일반 앞벽
        bpy.ops.mesh.primitive_cube_add(size=1, location=(
            0, -depth/2 + wall_thickness/2, floor_base_z + slab_thickness + wall_height/2
        ))
        front_wall = bpy.context.active_object
        front_wall.name = f"Floor_{floor_num}_Wall_Front"
        front_wall.scale = (width, wall_thickness, wall_height)
        front_wall.data.materials.append(materials['wall'])
        floor_objects.append(front_wall)

    # 우측벽
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        width/2 - wall_thickness/2, 0, floor_base_z + slab_thickness + wall_height/2
    ))
    right_wall = bpy.context.active_object
    right_wall.name = f"Floor_{floor_num}_Wall_Right"
    right_wall.scale = (wall_thickness, depth - wall_thickness*2, wall_height)
    right_wall.data.materials.append(materials['wall'])
    floor_objects.append(right_wall)

    # 좌측벽
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        -width/2 + wall_thickness/2, 0, floor_base_z + slab_thickness + wall_height/2
    ))
    left_wall = bpy.context.active_object
    left_wall.name = f"Floor_{floor_num}_Wall_Left"
    left_wall.scale = (wall_thickness, depth - wall_thickness*2, wall_height)
    left_wall.data.materials.append(materials['wall'])
    floor_objects.append(left_wall)

    # 창문 생성
    window_width = 1.2
    window_height = 1.5
    window_depth = wall_thickness + 0.02
    num_windows = max(1, int(width / 3))

    for i in range(num_windows):
        window_x = -width/2 + width/(num_windows+1) * (i+1)
        window_z = floor_base_z + slab_thickness + wall_height/2

        # 앞면 창문 - 1층 입구가 있으면 입구 영역 피하기
        if floor_num == 1 and entrance_width > 0:
            # 입구 영역 (-entrance_width/2 ~ entrance_width/2) 피하기
            if abs(window_x) > entrance_width/2 + window_width/2:
                bpy.ops.mesh.primitive_cube_add(
                    size=1,
                    location=(window_x, -depth/2 + wall_thickness/2, window_z)
                )
                window = bpy.context.active_object
                window.name = f"Floor_{floor_num}_Window_Front_{i}"
                window.scale = (window_width, window_depth, window_height)
                window.data.materials.append(materials['glass'])
                floor_objects.append(window)
        else:
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
                   wall_color=(0.85, 0.82, 0.78, 1.0), entrance_width=0):
    """건물 생성

    Args:
        entrance_width: 1층 입구 너비 (0이면 입구 없음)
    """
    materials = {
        'concrete': create_material(f"{name}_Concrete", (0.5, 0.5, 0.5, 1.0), roughness=0.9),
        'wall': create_material(f"{name}_Wall", wall_color, roughness=0.7),
        'glass': create_material(f"{name}_Glass", (0.6, 0.8, 0.9, 0.5), metallic=0.9, roughness=0.1),
        'roof': create_material(f"{name}_Roof", (0.3, 0.3, 0.35, 1.0), roughness=0.8),
    }

    building_objects = []

    for floor_num in range(1, num_floors + 1):
        floor_objects = create_floor(width, depth, floor_height, floor_num, materials,
                                     entrance_width=entrance_width if floor_num == 1 else 0)
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
    """건물 입구 생성 - 유리 도어문"""
    frame_mat = create_material(f"{building.name}_EntranceFrame",
                                (0.15, 0.15, 0.18, 1.0), metallic=0.9, roughness=0.2)
    glass_mat = create_material(f"{building.name}_DoorGlass",
                               (0.7, 0.85, 0.9, 0.3), metallic=0.1, roughness=0.05)
    handle_mat = create_material(f"{building.name}_DoorHandle",
                                (0.8, 0.8, 0.8, 1.0), metallic=1.0, roughness=0.1)

    entrance_objects = []
    frame_thickness = 0.05
    frame_depth = 0.08

    # 외부 프레임 - 상단
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth/2 + frame_depth/2, height))
    top_frame = bpy.context.active_object
    top_frame.name = f"{building.name}_Entrance_TopFrame"
    top_frame.scale = (width + frame_thickness*2, frame_depth, frame_thickness*2)
    top_frame.data.materials.append(frame_mat)
    top_frame.parent = building
    entrance_objects.append(top_frame)

    # 외부 프레임 - 좌측
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

    # 외부 프레임 - 우측
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

    # 유리 도어 (양쪽 여닫이)
    door_width = (width - 0.06) / 2
    door_height = height - 0.1

    for i, x_offset in enumerate([-door_width/2 - 0.015, door_width/2 + 0.015]):
        # 문 프레임
        door_frame_positions = [
            # 상단 프레임
            ((x_offset, -depth/2 + frame_depth/2, door_height), (door_width, 0.04, 0.06)),
            # 하단 프레임
            ((x_offset, -depth/2 + frame_depth/2, 0.03), (door_width, 0.04, 0.06)),
            # 좌측 프레임
            ((x_offset - door_width/2 + 0.02, -depth/2 + frame_depth/2, door_height/2), (0.04, 0.04, door_height)),
            # 우측 프레임
            ((x_offset + door_width/2 - 0.02, -depth/2 + frame_depth/2, door_height/2), (0.04, 0.04, door_height)),
        ]

        for j, (pos, scale) in enumerate(door_frame_positions):
            bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
            frame = bpy.context.active_object
            frame.name = f"{building.name}_DoorFrame_{i}_{j}"
            frame.scale = scale
            frame.data.materials.append(frame_mat)
            frame.parent = building
            entrance_objects.append(frame)

        # 유리 패널
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_offset, -depth/2 + frame_depth/2, door_height/2)
        )
        glass = bpy.context.active_object
        glass.name = f"{building.name}_DoorGlass_{i}"
        glass.scale = (door_width - 0.08, 0.02, door_height - 0.12)
        glass.data.materials.append(glass_mat)
        glass.parent = building
        entrance_objects.append(glass)

        # 문 손잡이
        handle_x = x_offset + (door_width/2 - 0.15) * (-1 if i == 0 else 1)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.02,
            depth=0.15,
            location=(handle_x, -depth/2 - 0.02, height * 0.45)
        )
        handle = bpy.context.active_object
        handle.name = f"{building.name}_DoorHandle_{i}"
        handle.rotation_euler = (math.pi/2, 0, 0)
        handle.data.materials.append(handle_mat)
        handle.parent = building
        entrance_objects.append(handle)

    # 중앙 세로 프레임
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -depth/2 + frame_depth/2, door_height/2)
    )
    center_frame = bpy.context.active_object
    center_frame.name = f"{building.name}_Entrance_CenterFrame"
    center_frame.scale = (0.04, frame_depth, door_height)
    center_frame.data.materials.append(frame_mat)
    center_frame.parent = building
    entrance_objects.append(center_frame)

    # 캐노피 (유리 지붕)
    canopy_mat = create_material(f"{building.name}_Canopy",
                                (0.2, 0.2, 0.22, 1.0), metallic=0.9, roughness=0.2)
    canopy_glass_mat = create_material(f"{building.name}_CanopyGlass",
                                      (0.8, 0.9, 0.95, 0.2), metallic=0.1, roughness=0.05)

    # 캐노피 프레임
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth/2 - 0.6, height + 0.15))
    canopy_frame = bpy.context.active_object
    canopy_frame.name = f"{building.name}_CanopyFrame"
    canopy_frame.scale = (width + 0.8, 1.0, 0.05)
    canopy_frame.data.materials.append(canopy_mat)
    canopy_frame.parent = building
    entrance_objects.append(canopy_frame)

    # 캐노피 유리
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -depth/2 - 0.6, height + 0.12))
    canopy_glass = bpy.context.active_object
    canopy_glass.name = f"{building.name}_CanopyGlass"
    canopy_glass.scale = (width + 0.6, 0.8, 0.02)
    canopy_glass.data.materials.append(canopy_glass_mat)
    canopy_glass.parent = building
    entrance_objects.append(canopy_glass)

    return entrance_objects
