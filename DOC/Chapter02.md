# Chapter 02. Python 런타임과 핵심 라이브러리

## Python

- Python 3.11을 기준으로 컨테이너 이미지를 구성했습니다.
- FastAPI/테스트 생태계와 호환성이 좋고, 현대적인 타입 힌트 및 성능 이점을 활용할 수 있습니다.

## 핵심 라이브러리 역할

- `fastapi`: REST API 및 정적 파일 제공
- `uvicorn`: ASGI 서버 실행
- `pydantic`: 응답 모델 검증
- `pytest`: 자동 테스트
- `httpx`: 테스트/클라이언트 요청 유틸

## 기존 스크립트 생태계 라이브러리

- `torch`, `diffusers`: 생성형 모델 추론
- `opencv-python`, `Pillow`, `numpy`: 영상/이미지 처리
- `controlnet_aux`, `transformers`: 조건부 생성 파이프라인 보조
