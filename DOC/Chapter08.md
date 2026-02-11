# Chapter 08. 테스트 전략과 품질 기준

## 자동 테스트

- `pytest` + FastAPI `TestClient`로 핵심 API 검증

## 테스트 항목

- `/api/health` 응답 코드/필드
- `/api/stack` 데이터 개수/구조
- `/api/files`에 기존 `.py` 스크립트가 노출되는지 확인

## 품질 기준

- 실패 시 원인 파악 가능한 메시지
- 스키마 변경 시 테스트 동반 업데이트
