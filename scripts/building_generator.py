"""
Blender Building Generator
1-3층 규모의 빌딩을 GLTF 형식으로 생성하는 스크립트
"""

import bpy
import math
import random
import os

# 출력 디렉토리 설정
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def clear_scene():
    """씬의 모든 오브젝트 삭제"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # 모든 메시, 머티리얼 등 정리
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)


def create_material(name, color, metallic=0.0, roughness=0.5):
    """머티리얼 생성"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return mat


def create_floor(width, depth, height, floor_num, materials):
    """단일 층 생성"""
    # 바닥/천장 두께
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
        # (위치, 스케일, 이름)
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

    # 창문 생성 (앞면과 뒷면에)
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

    # 각 층 생성
    for floor_num in range(1, num_floors + 1):
        floor_objects = create_floor(width, depth, floor_height, floor_num, materials)
        building_objects.extend(floor_objects)

    # 지붕 생성
    roof_z = num_floors * floor_height + 0.15
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, roof_z)
    )
    roof = bpy.context.active_object
    roof.name = f"{name}_Roof"
    roof.scale = (width + 0.3, depth + 0.3, 0.3)
    roof.data.materials.append(materials['roof'])
    building_objects.append(roof)

    # 모든 오브젝트를 하나의 부모로 묶기
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    parent = bpy.context.active_object
    parent.name = name

    for obj in building_objects:
        obj.parent = parent

    return parent


def create_text_on_roof_edge(text, building, width, depth, num_floors, floor_height,
                             text_color=(0.1, 0.1, 0.1, 1.0), text_size=1.0):
    """건물 지붕 가장자리에 텍스트 추가 (바닥 기준으로 세움)"""
    # 텍스트 커브 생성
    bpy.ops.object.text_add()
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = text_size
    text_obj.data.extrude = 0.08
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'BOTTOM'

    # 텍스트를 메시로 변환
    bpy.ops.object.convert(target='MESH')

    # 머티리얼 적용
    mat = create_material(f"{building.name}_RoofText_{text}", text_color, roughness=0.3)
    text_obj.data.materials.append(mat)

    # 지붕 높이 계산
    roof_z = num_floors * floor_height + 0.3

    # 지붕 앞쪽 가장자리 가운데에 배치 (글자가 앞을 향하도록)
    text_obj.location = (0, -depth/2 - 0.15, roof_z)
    text_obj.rotation_euler = (0, 0, 0)  # 글자가 똑바로 서있음

    text_obj.name = f"{building.name}_RoofText_{text}"
    text_obj.parent = building

    return text_obj


def create_text_on_wall(text, building, floor_num=1, wall_side="front",
                        text_color=(0.1, 0.1, 0.1, 1.0)):
    """건물 벽면에 텍스트 추가"""
    # 텍스트 커브 생성
    bpy.ops.object.text_add()
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = 0.8
    text_obj.data.extrude = 0.05
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    # 텍스트를 메시로 변환
    bpy.ops.object.convert(target='MESH')

    # 머티리얼 적용
    mat = create_material(f"{building.name}_Text_{text}", text_color, roughness=0.3)
    text_obj.data.materials.append(mat)

    # 건물 크기 계산 (자식 오브젝트들의 바운딩 박스 기반)
    floor_height = 3.5
    depth = 6

    # 위치 및 회전 설정
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
    # 입구 프레임
    frame_mat = create_material(f"{building.name}_EntranceFrame",
                                (0.2, 0.2, 0.25, 1.0), metallic=0.8)
    door_mat = create_material(f"{building.name}_Door",
                              (0.4, 0.25, 0.15, 1.0), roughness=0.6)

    entrance_objects = []

    # 문 프레임
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

    # 문 (두 개의 유리문)
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

    # 캐노피 (차양)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -depth/2 - 0.5, height + 0.2)
    )
    canopy = bpy.context.active_object
    canopy.name = f"{building.name}_Canopy"
    canopy.scale = (width + 1, 1.2, 0.1)
    canopy.data.materials.append(frame_mat)
    canopy.parent = building
    entrance_objects.append(canopy)

    return entrance_objects


def create_tree(location, height=4, name="Tree"):
    """나무 생성"""
    tree_objects = []

    # 트렁크 (기둥)
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

    # 나뭇잎 (여러 구체)
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

    # 부모 오브젝트 생성
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent = bpy.context.active_object
    parent.name = name

    for obj in tree_objects:
        obj.parent = parent

    return parent


def create_road(length=30, width=6, location=(0, -15, 0)):
    """도로 생성"""
    road_objects = []

    # 도로 머티리얼
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

    # 인도 (양쪽)
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

    # 부모 오브젝트 생성
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    parent = bpy.context.active_object
    parent.name = "Road"

    for obj in road_objects:
        obj.parent = parent

    return parent


def export_to_gltf(filepath, export_format='GLTF_SEPARATE'):
    """GLTF 형식으로 내보내기"""
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format=export_format,
        export_apply=True,
        export_materials='EXPORT'
    )
    print(f"Exported to: {filepath}")


def create_building_scene_1():
    """씬 1: 기본 2층 건물 + 텍스트 + 입구"""
    clear_scene()

    building = create_building(
        "Building_Basic",
        width=10, depth=8, floor_height=3.5, num_floors=2,
        wall_color=(0.9, 0.85, 0.75, 1.0)
    )

    create_text_on_wall("TEST", building, floor_num=2, wall_side="front")
    create_entrance(building, width=2.5, height=2.8, depth=8)

    # 나무 추가
    create_tree(location=(-7, -2, 0), height=5, name="Tree_1")
    create_tree(location=(7, -2, 0), height=4, name="Tree_2")

    export_to_gltf(os.path.join(OUTPUT_DIR, "building_basic.gltf"))


def create_building_scene_2():
    """씬 2: 3층 오피스 빌딩 + 도로"""
    clear_scene()

    building = create_building(
        "Office_Building",
        width=12, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.7, 0.75, 0.8, 1.0)
    )

    create_text_on_wall("OFFICE", building, floor_num=3, wall_side="front",
                       text_color=(0.1, 0.2, 0.4, 1.0))
    create_entrance(building, width=3, height=3, depth=10)

    # 도로
    create_road(length=40, width=8, location=(0, -18, 0))

    # 나무들
    for i, x in enumerate([-12, -8, 8, 12]):
        create_tree(location=(x, -8, 0), height=random.uniform(3.5, 5.5),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "office_building.gltf"))


def create_building_scene_3():
    """씬 3: 1층 상점 건물"""
    clear_scene()

    width, depth, floor_height, num_floors = 8, 6, 4, 1

    building = create_building(
        "Shop_Building",
        width=width, depth=depth, floor_height=floor_height, num_floors=num_floors,
        wall_color=(0.95, 0.9, 0.8, 1.0)
    )

    # 지붕 가장자리에 SHOP 텍스트 추가
    create_text_on_roof_edge("SHOP", building, width=width, depth=depth,
                             num_floors=num_floors, floor_height=floor_height,
                             text_color=(0.8, 0.2, 0.1, 1.0), text_size=1.2)
    create_entrance(building, width=3, height=2.8, depth=depth)

    # 나무
    create_tree(location=(-6, 0, 0), height=3.5, name="Tree_1")

    export_to_gltf(os.path.join(OUTPUT_DIR, "shop_building.gltf"))


def create_building_scene_4():
    """씬 4: 도시 블록 - 여러 건물"""
    clear_scene()

    # 건물 1: 2층 아파트
    building1 = create_building(
        "Apartment_1",
        width=10, depth=8, floor_height=3, num_floors=2,
        wall_color=(0.85, 0.8, 0.7, 1.0)
    )
    building1.location = (-15, 0, 0)
    create_text_on_wall("APT", building1, floor_num=2, wall_side="front")

    # 건물 2: 3층 오피스
    building2 = create_building(
        "Office_1",
        width=12, depth=10, floor_height=3.5, num_floors=3,
        wall_color=(0.75, 0.78, 0.85, 1.0)
    )
    building2.location = (5, 0, 0)
    create_text_on_wall("CORP", building2, floor_num=3, wall_side="front",
                       text_color=(0.15, 0.25, 0.5, 1.0))
    create_entrance(building2, width=3, height=3, depth=10)

    # 건물 3: 1층 카페
    building3 = create_building(
        "Cafe",
        width=6, depth=5, floor_height=3.5, num_floors=1,
        wall_color=(0.9, 0.85, 0.75, 1.0)
    )
    building3.location = (22, 0, 0)
    create_text_on_wall("CAFE", building3, floor_num=1, wall_side="front",
                       text_color=(0.6, 0.3, 0.1, 1.0))

    # 도로
    create_road(length=60, width=8, location=(0, -18, 0))

    # 나무들
    tree_positions = [(-20, -8), (-10, -8), (0, -8), (10, -8), (20, -8)]
    for i, pos in enumerate(tree_positions):
        create_tree(location=(pos[0], pos[1], 0),
                   height=random.uniform(3, 5),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "city_block.gltf"))


def create_building_scene_5():
    """씬 5: 모던 스타일 건물"""
    clear_scene()

    building = create_building(
        "Modern_Building",
        width=14, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.25, 0.28, 0.32, 1.0)  # 다크 그레이
    )

    create_text_on_wall("MODERN", building, floor_num=2, wall_side="front",
                       text_color=(0.9, 0.9, 0.9, 1.0))  # 흰색 텍스트
    create_entrance(building, width=4, height=3.5, depth=10)

    # 도로
    create_road(length=45, width=8, location=(0, -20, 0))

    # 나무들
    for i in range(6):
        x = -15 + i * 6
        create_tree(location=(x, -10, 0), height=random.uniform(4, 6),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "modern_building.gltf"))


def main():
    """메인 함수 - 모든 씬 생성"""
    print("="*50)
    print("Building Generator Started")
    print("="*50)

    # 출력 디렉토리 확인
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 모든 씬 생성
    print("\n[1/5] Creating Basic Building Scene...")
    create_building_scene_1()

    print("\n[2/5] Creating Office Building Scene...")
    create_building_scene_2()

    print("\n[3/5] Creating Shop Building Scene...")
    create_building_scene_3()

    print("\n[4/5] Creating City Block Scene...")
    create_building_scene_4()

    print("\n[5/5] Creating Modern Building Scene...")
    create_building_scene_5()

    print("\n" + "="*50)
    print("All buildings generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*50)


if __name__ == "__main__":
    main()
