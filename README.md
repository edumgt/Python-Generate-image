# python-generate-image

간단한 Python 기반 이미지/영상 생성 실험 저장소입니다.  
`diffusers`와 `torch`를 이용해 텍스트→이미지, 이미지→이미지, 포즈 기반 영상 프레임 생성, ffmpeg 후처리(영상 합성/오디오 병합)를 수행합니다.

## 기술 스택

- **언어**: Python 3
- **AI/생성 모델**:
  - `diffusers` (Stable Diffusion, Img2Img, ControlNet Pipeline)
  - `torch` (CUDA/CPU 실행)
  - Hugging Face 모델 허브 모델 사용
- **컴퓨터 비전/이미지 처리**:
  - `opencv-python` (`cv2`) - 프레임 기반 영상 생성
  - `Pillow` (`PIL`) - 이미지 입출력/리사이즈
  - `numpy`
- **포즈/조건부 생성**:
  - `controlnet_aux` (`OpenposeDetector`)
  - ControlNet (`lllyasviel/sd-controlnet-openpose`)
- **미디어 파이프라인**:
  - `ffmpeg` (프레임↔영상 변환, FPS 변환, 오디오 병합)
  - `subprocess` 기반 외부 명령 호출
- **기타**:
  - `transformers` (`CLIPImageProcessor` 일부 스크립트에서 사용)

## 파일 구성

- `1.py`: 텍스트 프롬프트 기반 이미지 프레임 생성 후 mp4 저장
- `3.py`: 챔피언 프롬프트 기반 이미지 생성
- `cpu.py`, `cuda.py`, `cuda2.py`, `cuda3.py`, `cuda22.py`: 다양한 생성 파이프라인 실험 스크립트
- `cuda2_rife.py`, `cuda2_rife_v2.py`: 프레임 생성 후 보간/합성(고FPS/오디오 결합)
- `mp4make.py`: 프레임 기반 영상 생성 및 합성 유틸 성격 스크립트
- `imgwork.py`: 다수 프롬프트 배치 생성 스크립트

## 실행 환경 메모

1. CUDA GPU가 있으면 `torch.float16` + `cuda` 경로를 사용하고, 없으면 CPU 경로(`float32`)를 사용합니다.
2. 일부 스크립트는 대량 프레임을 생성하므로 VRAM/디스크 여유 공간이 필요합니다.
3. ffmpeg가 설치되어 있어야 영상 합성 스크립트가 정상 동작합니다.

## 보안/콘텐츠 정리 사항

- 저장소 내 하드코딩된 Hugging Face 토큰은 마스킹 처리되었고, 아래 형태로 환경변수 사용을 권장합니다.
  - `HF_TOKEN = os.getenv("HF_TOKEN", "hf_***MASKED***")`
- 부적절한(음란성) 프롬프트는 일반/비음란 프롬프트로 교체했습니다.

## 빠른 시작 예시

```bash
python3 -m venv .venv
source .venv/bin/activate
export HF_TOKEN="hf_your_real_token"
python 3.py
```

필요 시 각 스크립트 내 `model_id`, `prompt`, `fps`, `width/height`, `num_frames`를 목적에 맞게 조정하세요.
