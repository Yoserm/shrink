import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    store: str
    base_url: str
    db_url: str

    def __init__(self):
        self.store = os.getenv("SHRINK_STORE")
        self.base_url = os.getenv("SHRINK_BASE_URL")
        self.db_url = os.getenv("SHRINK_DB_URL")

        if not self.store:
            raise ValueError("SHRINK_STORE is required")

        if not self.base_url:
            raise ValueError("SHRINK_BASE_URL is required")

        if not self.db_url:
            raise ValueError("SHRINK_DB_URL is required")


settings = Settings()