from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "Your Mongodb string here"
    MONGODB_DB_NAME: str = "website_monitor"
    DEFAULT_CHECK_INTERVAL: int = 300  # 5 minutes in seconds
    DISCORD_WEBHOOK_URL: str = "Your discord webhook url here"

settings = Settings()

