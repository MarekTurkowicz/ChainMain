from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""

    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"

    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

    upload_dir: str = "data/uploads"
    chroma_dir: str = "data/chroma"
    metadata_file: str = "data/documents.json"

    frontend_origin: str = "http://localhost:9001"

    def _resolve(self, p: str) -> Path:
        path = Path(p)
        return path if path.is_absolute() else BACKEND_DIR / path

    @property
    def upload_path(self) -> Path:
        return self._resolve(self.upload_dir)

    @property
    def chroma_path(self) -> Path:
        return self._resolve(self.chroma_dir)

    @property
    def metadata_path(self) -> Path:
        return self._resolve(self.metadata_file)


settings = Settings()

settings.upload_path.mkdir(parents=True, exist_ok=True)
settings.chroma_path.mkdir(parents=True, exist_ok=True)
