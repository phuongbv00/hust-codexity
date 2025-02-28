from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_model: str
    openai_api_key: str
    local_api_key: str
    local_base_url: str

    model_config = SettingsConfigDict(env_file=".env")