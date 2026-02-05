"""Blender에서 실행할 스크립트"""
import sys
import os

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scripts.scenes import create_combined_scene

create_combined_scene()
