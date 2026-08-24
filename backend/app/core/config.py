

from pathlib import Path

from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_NAME: str = "AgriAI Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    MODEL_PATH: str = "models/best_vit_b16.pt"

    CONFIDENCE_THRESHOLD: float = 0.70
    TOP2_MARGIN_THRESHOLD: float = 0.20
    TOP_K: int = 3
    LEAF_VALIDATION_THRESHOLD: float = 0.80

    GEMINI_API_KEY: str

    @field_validator("GEMINI_API_KEY", mode="before")
    @classmethod
    def normalize_gemini_api_key(cls, value: object) -> str:
        if value is None:
            raise ValueError("Gemini API key is not configured.")

        if not isinstance(value, str):
            raise ValueError("Gemini API key is not configured.")

        normalized = value.strip()

        if (
            len(normalized) >= 2
            and normalized[0] == normalized[-1]
            and normalized[0] in {"\"", "'"}
        ):
            normalized = normalized[1:-1].strip()

        if not normalized:
            raise ValueError("Gemini API key is not configured.")

        return normalized

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()