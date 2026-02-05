# Blender Building Generator

Blender를 사용하여 1-3층 규모의 빌딩을 GLTF 형식으로 생성하는 프로젝트입니다.

## 프로젝트 구조

```
blender-building/
├── config/                     # 설정 파일
│   └── scene_config.json       # 씬 설정 (건물, 나무, 도로 등)
├── scripts/                    # Python 스크립트
│   ├── __init__.py
│   ├── building_generator.py   # 메인 진입점
│   ├── utils.py                # 유틸리티 함수
│   ├── building.py             # 건물 생성 함수
│   ├── environment.py          # 환경 요소 (나무, 도로)
│   └── scenes.py               # 씬 생성 함수
├── output/                     # 생성된 GLTF 파일
│   └── combined_scene.gltf     # 모든 건물이 포함된 통합 씬
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
blender --background --python -c "from scripts.scenes import create_combined_scene; create_combined_scene()"
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

## 생성되는 씬

통합 씬(`combined_scene.gltf`)에 다음 건물들이 포함됩니다:

- **Office Building** (왼쪽): 3층 오피스 빌딩
- **Shop Building** (가운데): 1층 상점 + 지붕 간판
- **Modern Building** (오른쪽): 3층 모던 스타일 건물
- **도로**: 전체 건물 앞을 지나는 도로
- **나무**: 건물 주변에 배치된 나무들

## 웹 뷰어 조작

- **좌클릭 + 드래그**: 회전
- **우클릭 + 드래그**: 이동
- **스크롤**: 줌

## JSON 설정 파일

`config/scene_config.json` 파일을 수정하여 씬을 커스터마이즈할 수 있습니다.

### 설정 예시

```json
{
  "scene": {
    "name": "my_scene",
    "ground": { "color": [0.23, 0.35, 0.25], "size": 200 }
  },
  "buildings": [
    {
      "name": "Office_Building",
      "position": [-25, 0],
      "floors": 3,
      "width": 12,
      "depth": 10,
      "floorHeight": 4,
      "wallColor": [0.7, 0.75, 0.8],
      "text": "OFFICE",
      "textColor": [0.1, 0.2, 0.4],
      "textPosition": "wall",
      "textFloor": 3,
      "entrance": { "width": 3, "height": 3 }
    }
  ],
  "road": {
    "enabled": true,
    "length": 80,
    "width": 8,
    "position": [0, -18, 0]
  },
  "trees": [
    { "position": [-35, -8], "height": 4.5 },
    { "position": [35, -8], "height": 5.2 }
  ]
}
```

### 설정 옵션

| 항목 | 설명 |
|------|------|
| `buildings[].position` | 건물 위치 [x, y] |
| `buildings[].floors` | 층 수 |
| `buildings[].wallColor` | 벽 색상 [r, g, b] (0-1) |
| `buildings[].textPosition` | 텍스트 위치 ("wall" 또는 "roof") |
| `road.enabled` | 도로 활성화 여부 |
| `trees[].position` | 나무 위치 [x, y] |
| `trees[].height` | 나무 높이 |
