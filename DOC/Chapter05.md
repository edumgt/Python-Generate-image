# Chapter 05. FastAPI 백엔드 아키텍처

새 백엔드는 기존 스크립트를 직접 대체하기보다, **스택 정보를 API로 노출하고 UI를 제공하는 관문 레이어**로 설계했습니다.

## 엔드포인트

- `GET /api/health`: 상태 확인
- `GET /api/stack`: 저장소 기술 스택 상세 정보
- `GET /api/files`: 루트 Python 스크립트 목록

## 설계 포인트

- 타입 안정성을 위한 Pydantic 모델 사용
- CORS 허용(로컬 개발 편의)
- 정적 파일(`frontend/`)을 루트(`/`)에 서빙
