# Blender Building Generator

Blender를 사용하여 1-3층 규모의 빌딩을 GLTF 형식으로 생성하는 프로젝트입니다.

## 프로젝트 구조

```
blender-building/
├── scripts/                    # Python 스크립트
│   ├── __init__.py
│   ├── building_generator.py   # 메인 진입점
│   ├── utils.py                # 유틸리티 함수
│   ├── building.py             # 건물 생성 함수
│   ├── environment.py          # 환경 요소 (나무, 도로)
│   └── scenes.py               # 씬 생성 함수
├── output/                     # 생성된 GLTF 파일
│   ├── office_building.gltf
│   ├── shop_building.gltf
│   └── modern_building.gltf
├── src/                        # React 웹 뷰어
│   ├── App.jsx
│   └── components/
├── requirements.txt
└── package.json
```

## 사용 라이브러리

### Python (Blender 스크립트)

| 라이브러리 | 버전 | 설명 |
|-----------|------|------|
| bpy | Blender 내장 | Blender Python API |
| os | 표준 라이브러리 | 파일 경로 처리 |
| math | 표준 라이브러리 | 수학 연산 (회전 등) |
| random | 표준 라이브러리 | 랜덤 값 생성 |

### JavaScript (웹 뷰어)

| 라이브러리 | 설명 |
|-----------|------|
| React | UI 프레임워크 |
| @react-three/fiber | React용 Three.js 렌더러 |
| @react-three/drei | Three.js 헬퍼 컴포넌트 |
| Three.js | 3D 그래픽 라이브러리 |

## 실행 방법

### 1. Blender에서 모델 생성

```bash
# Blender CLI로 실행
blender --background --python -c "from scripts.scenes import create_office_scene, create_shop_scene, create_modern_scene; create_office_scene(); create_shop_scene(); create_modern_scene()"
```

또는 Blender GUI에서:
1. Blender 실행
2. Scripting 워크스페이스로 이동
3. 스크립트 실행

### 2. 웹 뷰어 실행

```bash
# 의존성 설치
pnpm install

# 개발 서버 실행
pnpm dev
```

## 생성되는 건물

- **Office Building**: 3층 오피스 빌딩 + 도로 + 나무
- **Shop Building**: 1층 상점 + 지붕 간판
- **Modern Building**: 3층 모던 스타일 건물 + 도로 + 나무

## 웹 뷰어 조작

- **좌클릭 + 드래그**: 회전
- **우클릭 + 드래그**: 이동
- **스크롤**: 줌
