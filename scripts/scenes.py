"""씬 생성 함수들"""

import os
import json

from .utils import OUTPUT_DIR, clear_scene, export_to_gltf
from .building import create_building, create_text_on_wall, create_text_on_roof_edge, create_entrance
from .environment import create_tree, create_road

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")


def load_config(config_name="scene_config.json"):
    """JSON 설정 파일 로드"""
    config_path = os.path.join(CONFIG_DIR, config_name)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_scene_from_config(config_name="scene_config.json"):
    """JSON 설정 파일 기반으로 씬 생성"""
    config = load_config(config_name)
    clear_scene()

    scene_config = config.get("scene", {})
    scene_name = scene_config.get("name", "scene")

    # 건물 생성
    for building_config in config.get("buildings", []):
        building = create_building(
            building_config.get("name", "Building"),
            width=building_config.get("width", 10),
            depth=building_config.get("depth", 8),
            floor_height=building_config.get("floorHeight", 3.5),
            num_floors=building_config.get("floors", 2),
            wall_color=tuple(building_config.get("wallColor", [0.85, 0.82, 0.78])) + (1.0,)
        )

        # 위치 설정
        pos = building_config.get("position", [0, 0])
        building.location = (pos[0], pos[1], 0)

        # 텍스트 추가
        text = building_config.get("text")
        if text:
            text_color = tuple(building_config.get("textColor", [0.1, 0.1, 0.1])) + (1.0,)
            text_position = building_config.get("textPosition", "wall")

            if text_position == "roof":
                create_text_on_roof_edge(
                    text, building,
                    width=building_config.get("width", 10),
                    depth=building_config.get("depth", 8),
                    num_floors=building_config.get("floors", 2),
                    floor_height=building_config.get("floorHeight", 3.5),
                    text_color=text_color,
                    text_size=building_config.get("textSize", 1.0)
                )
            else:
                create_text_on_wall(
                    text, building,
                    floor_num=building_config.get("textFloor", 1),
                    wall_side="front",
                    text_color=text_color
                )

        # 입구 추가
        entrance = building_config.get("entrance")
        if entrance:
            create_entrance(
                building,
                width=entrance.get("width", 2),
                height=entrance.get("height", 2.5),
                depth=building_config.get("depth", 8)
            )

    # 도로 생성
    road_config = config.get("road", {})
    if road_config.get("enabled", True):
        road_pos = road_config.get("position", [0, -18, 0])
        create_road(
            length=road_config.get("length", 40),
            width=road_config.get("width", 8),
            location=tuple(road_pos)
        )

    # 나무 생성
    for i, tree_config in enumerate(config.get("trees", [])):
        pos = tree_config.get("position", [0, 0])
        create_tree(
            location=(pos[0], pos[1], 0),
            height=tree_config.get("height", 4),
            name=f"Tree_{i}"
        )

    # 내보내기
    output_file = os.path.join(OUTPUT_DIR, f"{scene_name}.gltf")
    export_to_gltf(output_file)


def create_combined_scene():
    """기본 설정으로 통합 씬 생성"""
    create_scene_from_config("scene_config.json")
