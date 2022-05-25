import json


class Settings:
    PROJECT_NAME: str = "Shop Cards"
    PROJECT_VERSION: str = "1.1.2"

    with open("secrets.json") as f:
        secrets = json.load(f)["config"]
    SECRET_KEY: str = secrets["SECRET_KEY"]
    ALGORITHM = secrets["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = 3 * 30 * 24 * 60  # 3 months


settings = Settings()
