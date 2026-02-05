"""씬 생성 함수들"""

import os
import random

from .utils import OUTPUT_DIR, clear_scene, export_to_gltf
from .building import create_building, create_text_on_wall, create_text_on_roof_edge, create_entrance
from .environment import create_tree, create_road


def create_combined_scene():
    """모든 건물을 하나의 씬에 배치"""
    clear_scene()

    # Office Building (왼쪽)
    office = create_building(
        "Office_Building",
        width=12, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.7, 0.75, 0.8, 1.0)
    )
    office.location = (-25, 0, 0)
    create_text_on_wall("OFFICE", office, floor_num=3, wall_side="front",
                       text_color=(0.1, 0.2, 0.4, 1.0))
    create_entrance(office, width=3, height=3, depth=10)

    # Shop Building (가운데)
    width, depth, floor_height, num_floors = 8, 6, 4, 1
    shop = create_building(
        "Shop_Building",
        width=width, depth=depth, floor_height=floor_height, num_floors=num_floors,
        wall_color=(0.95, 0.9, 0.8, 1.0)
    )
    shop.location = (0, 0, 0)
    create_text_on_roof_edge("SHOP", shop, width=width, depth=depth,
                             num_floors=num_floors, floor_height=floor_height,
                             text_color=(0.8, 0.2, 0.1, 1.0), text_size=1.2)
    create_entrance(shop, width=3, height=2.8, depth=depth)

    # Modern Building (오른쪽)
    modern = create_building(
        "Modern_Building",
        width=14, depth=10, floor_height=4, num_floors=3,
        wall_color=(0.25, 0.28, 0.32, 1.0)
    )
    modern.location = (25, 0, 0)
    create_text_on_wall("MODERN", modern, floor_num=2, wall_side="front",
                       text_color=(0.9, 0.9, 0.9, 1.0))
    create_entrance(modern, width=4, height=3.5, depth=10)

    # 도로 (전체 앞쪽)
    create_road(length=80, width=8, location=(0, -18, 0))

    # 나무들
    tree_positions = [
        (-35, -8), (-20, -8), (-10, -8), (10, -8), (20, -8), (35, -8),
        (-30, 8), (-15, 8), (0, 8), (15, 8), (30, 8)
    ]
    for i, pos in enumerate(tree_positions):
        create_tree(location=(pos[0], pos[1], 0),
                   height=random.uniform(3.5, 5.5),
                   name=f"Tree_{i}")

    export_to_gltf(os.path.join(OUTPUT_DIR, "combined_scene.gltf"))
