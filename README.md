# python-generate-image

간단한 Python 기반 이미지/영상 생성 실험 저장소입니다.  
`diffusers`와 `torch`를 이용해 텍스트→이미지, 이미지→이미지, 포즈 기반 영상 프레임 생성, ffmpeg 후처리(영상 합성/오디오 병합)를 수행합니다.

## 기술 문서

상세 기술 스택 문서는 `DOC/Chapter01.md` ~ `DOC/Chapter10.md`를 참고하세요.

## 웹 대시보드 (FastAPI + Vanilla JS)

- 백엔드: FastAPI
- 프런트엔드: Vanilla JS (정적 파일)
- 주요 API
  - `GET /api/health`
  - `GET /api/stack`
  - `GET /api/files`

## 로컬 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

브라우저에서 `http://localhost:8000` 접속.

## Docker 실행

```bash
docker compose up --build
```

브라우저에서 `http://localhost:8000` 접속.

## 테스트

```bash
pytest -q
```
