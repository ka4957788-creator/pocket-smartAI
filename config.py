from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str='PocketSmart AI'; secret_key:str='change-me'; gemini_api_key:str=''; gemini_model:str='gemini-3.8-flash'; access_token_expire_minutes:int=1440; database_path:str='./data/pocketsmart.db'; max_upload_mb:int=5
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
@lru_cache
def get_settings(): return Settings()
