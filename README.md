# ai-sprint-missions

AI 스프린트 미션 및 실험 프로젝트들을 하나로 모은 모노레포입니다.
각 프로젝트는 자체 의존성(`requirements.txt` 등)을 그대로 유지하여 **독립 실행 가능**합니다.

> 원본: [github.com/chung2000](https://github.com/chung2000) 의 개별 저장소 7개 (커밋 히스토리 미보존, 스냅샷 통합)

## 디렉터리 구조

| 카테고리 | 설명 |
|----------|------|
| [`missions/`](missions/) | 스프린트 미션 결과물 (15~18) |
| [`experiments/`](experiments/) | 실험·실습용 단발성 프로젝트 |

## 프로젝트 목록 (7개)

### missions/ — 스프린트 미션
| 프로젝트 | 스택 | 설명 |
|----------|------|------|
| [mission_15](missions/mission_15) | Docker Compose · scikit-learn · Jupyter | Docker 기반 ML 협업 파이프라인 (학습-추론 자동화, Student Performance 회귀) |
| [mission_16](missions/mission_16) | Jupyter | 모델링/추론 노트북 (modeling.ipynb, inference.ipynb) |
| [mission_17](missions/mission_17) | Streamlit · 객체탐지 · QWEN | Hybrid Vision AI — 멀티태스크 이미지 분석기 |
| [mission_18](missions/mission_18) | Streamlit · FastAPI · 감성분석 | AI 기반 영화 리뷰 감성 분석 웹 서비스 |
| [mission18_vercel](missions/mission18_vercel) | Vercel · Python | mission_18 의 Vercel 배포 변형 |

### experiments/ — 실험/실습
| 프로젝트 | 스택 | 설명 |
|----------|------|------|
| [sprint-ai05-git](experiments/sprint-ai05-git) | Python | API 요청/응답 실습 (main, web, request, response) |
| [streamlit_test](experiments/streamlit_test) | Streamlit | 대시보드 실험 (1_dashboard.py) |

## 실행 방법

각 프로젝트 디렉터리로 이동하여 자체 의존성을 설치 후 실행합니다.

```bash
cd missions/mission_18
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# 예) Streamlit 앱
streamlit run frontend/app.py
```

> 프로젝트마다 요구 패키지/실행 진입점이 다릅니다. 각 프로젝트의 README를 함께 참고하세요.
