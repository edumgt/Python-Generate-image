from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"


class HealthResponse(BaseModel):
    status: str


class StackItem(BaseModel):
    name: str
    category: str
    description: str


class FilesResponse(BaseModel):
    python_files: list[str]


app = FastAPI(title="python-generate-image dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/stack", response_model=list[StackItem])
def stack() -> list[StackItem]:
    return [
        StackItem(name="Python 3", category="Language", description="Core runtime for scripts and API service."),
        StackItem(name="FastAPI", category="Backend", description="REST API and static file serving."),
        StackItem(name="Vanilla JavaScript", category="Frontend", description="Lightweight browser UI without framework."),
        StackItem(name="PyTorch", category="AI", description="Tensor runtime for CPU/GPU inference."),
        StackItem(name="Diffusers", category="AI", description="Stable Diffusion and related image generation pipelines."),
        StackItem(name="OpenCV/Pillow", category="Media", description="Frame and image processing utilities."),
        StackItem(name="FFmpeg", category="Media", description="Video encoding and audio merge pipeline."),
        StackItem(name="Docker", category="DevOps", description="Container-based local execution and testing."),
    ]


@app.get("/api/files", response_model=FilesResponse)
def files() -> FilesResponse:
    python_files = sorted(path.name for path in BASE_DIR.glob("*.py"))
    return FilesResponse(python_files=python_files)


if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
