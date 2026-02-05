"""
Blender Building Generator
1-3층 규모의 빌딩을 GLTF 형식으로 생성하는 스크립트
"""

import os
from .utils import OUTPUT_DIR
from .scenes import create_office_scene, create_shop_scene, create_modern_scene


def main():
    """메인 함수 - 모든 씬 생성"""
    print("="*50)
    print("Building Generator Started")
    print("="*50)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n[1/3] Creating Office Building Scene...")
    create_office_scene()

    print("\n[2/3] Creating Shop Building Scene...")
    create_shop_scene()

    print("\n[3/3] Creating Modern Building Scene...")
    create_modern_scene()

    print("\n" + "="*50)
    print("All buildings generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*50)


if __name__ == "__main__":
    main()
