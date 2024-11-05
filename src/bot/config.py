from pydantic import SecretStr
from pydantic_settings import BaseSettings

from bot.internal.config_dicts import assign_config_dict
from bot.internal.enums import Stage


class BotConfig(BaseSettings):
    STAGE: Stage
    ADMINS: list[int]
    TOKEN: SecretStr
    SENTRY_DSN: SecretStr | None = None
    SUPPORT_CHAT_LINK: str

    model_config = assign_config_dict(prefix="BOT_")


class DBConfig(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    NAME: str
    HOST: str
    PORT: int
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    model_config = assign_config_dict(prefix="DB_")

    @property
    def get_db_connection_string(self):
        return SecretStr(
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASSWORD.get_secret_value()}@"
            f"{self.HOST}:{self.PORT}/{self.NAME}"
        )


class MarzbanConfig(BaseSettings):
    BASE_URL: str
    ADMIN: str
    PASSWORD: SecretStr

    model_config = assign_config_dict(prefix="MARZBAN_")


class Settings(BaseSettings):
    bot: BotConfig = BotConfig()
    db: DBConfig = DBConfig()
    marzban: MarzbanConfig = MarzbanConfig()

    model_config = assign_config_dict()


settings = Settings()
