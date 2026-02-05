"""
Blender Building Generator
1-3층 규모의 빌딩을 GLTF 형식으로 생성하는 스크립트
"""

import os
from .utils import OUTPUT_DIR
from .scenes import create_combined_scene


def main():
    """메인 함수 - 통합 씬 생성"""
    print("="*50)
    print("Building Generator Started")
    print("="*50)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\nCreating Combined Scene...")
    create_combined_scene()

    print("\n" + "="*50)
    print("Scene generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*50)


if __name__ == "__main__":
    main()
