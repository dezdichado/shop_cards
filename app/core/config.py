import os

class Settings:
    PROJECT_NAME: str = "Shop Cards"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT",
                                   5432)  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")

    SECRET_KEY: str = "qergkq5egn4"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 3 * 30 * 24 * 60  # 3 months


settings = Settings()
