from pydantic import BaseSettings, validator
from typing_extensions import Literal
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "Abnormal Request Identifier"
    API_PREFIX: str = "/local"
    API_PORT: Optional[int] = 8001
    DATA_STORAGE_MODE: Literal["db_storage", "file_storage"] = "file_storage"
    RUN_ENV: Literal["dev", "deploy"] = "dev"
    APP_RELOAD: Optional[bool]

    @validator("APP_RELOAD", pre=True)
    def get_app_reload(cls, v, values: Dict[str, Any]) -> bool:
        if v:
            return v
        else:
            run_env = values.get("RUN_ENV")
            return True if run_env == "dev" else False


settings = Settings(_env_file=".env")
