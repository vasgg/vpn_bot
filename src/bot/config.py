from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from bot.internal.enums import Stage


class BotConfig(BaseSettings):
    STAGE: Stage
    ADMIN_ID: int
    TOKEN: SecretStr
    SENTRY_DSN: SecretStr | None = None

    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        env_file='.env',
        extra='allow',
    )


class DBConfig(BaseSettings):
    USER: str
    PASSWORD: SecretStr
    NAME: str
    HOST: str
    PORT: int
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file='.env',
        extra='allow',
    )

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

    model_config = SettingsConfigDict(
        env_prefix="MARZBAN_",
        env_file='.env',
        extra='allow',
    )


class Settings(BaseSettings):
    bot: BotConfig
    db: DBConfig
    marzban: MarzbanConfig

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='allow',
    )


settings = Settings(bot=BotConfig(), db=DBConfig(), marzban=MarzbanConfig())
