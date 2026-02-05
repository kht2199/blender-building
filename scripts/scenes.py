"""씬 생성 함수들"""

import os
import random

from .utils import OUTPUT_DIR, clear_scene, export_to_gltf
from .building import create_building, create_text_on_wall, create_text_on_roof_edge, create_entrance
from .environment import create_tree, create_road


def create_office_scene():
    """오피스 빌딩 씬"""
    clear_scene()

    building = create_building(
        "Office_Building",
        width=12, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.7, 0.75, 0.8, 1.0)
    )

    create_text_on_wall("OFFICE", building, floor_num=3, wall_side="front",
                       text_color=(0.1, 0.2, 0.4, 1.0))
    create_entrance(building, width=3, height=3, depth=10)

    create_road(length=40, width=8, location=(0, -18, 0))

    for i, x in enumerate([-12, -8, 8, 12]):
        create_tree(location=(x, -8, 0), height=random.uniform(3.5, 5.5),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "office_building.gltf"))


def create_shop_scene():
    """상점 빌딩 씬"""
    clear_scene()

    width, depth, floor_height, num_floors = 8, 6, 4, 1

    building = create_building(
        "Shop_Building",
        width=width, depth=depth, floor_height=floor_height, num_floors=num_floors,
        wall_color=(0.95, 0.9, 0.8, 1.0)
    )

    create_text_on_roof_edge("SHOP", building, width=width, depth=depth,
                             num_floors=num_floors, floor_height=floor_height,
                             text_color=(0.8, 0.2, 0.1, 1.0), text_size=1.2)
    create_entrance(building, width=3, height=2.8, depth=depth)

    create_tree(location=(-6, 0, 0), height=3.5, name="Tree_1")

    export_to_gltf(os.path.join(OUTPUT_DIR, "shop_building.gltf"))


def create_modern_scene():
    """모던 빌딩 씬"""
    clear_scene()

    building = create_building(
        "Modern_Building",
        width=14, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.25, 0.28, 0.32, 1.0)
    )

    create_text_on_wall("MODERN", building, floor_num=2, wall_side="front",
                       text_color=(0.9, 0.9, 0.9, 1.0))
    create_entrance(building, width=4, height=3.5, depth=10)

    create_road(length=45, width=8, location=(0, -20, 0))

    for i in range(6):
        x = -15 + i * 6
        create_tree(location=(x, -10, 0), height=random.uniform(4, 6),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "modern_building.gltf"))
