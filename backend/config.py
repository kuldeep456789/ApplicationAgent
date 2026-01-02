from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    database_url: str = "sqlite+aiosqlite:///./data/job_assistant.db"
    redis_url: Optional[str] = None
    app_env: str = "development"
    log_level: str = "INFO"
    debug: bool = True
    llm_provider: str = "gemini"  
    headless_browser: bool = True
    browser_timeout: int = 30000
    max_requests_per_minute: int = 10
    scraper_delay_seconds: int = 2
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    user_location: Optional[str] = None
    sentry_dsn: Optional[str] = None
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8501"]
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"
settings = Settings()
