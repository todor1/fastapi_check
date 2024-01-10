from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    The empty ENV_STATE allows us to get that value from the .env file.
    It is not going to look in other  variables prefixed with the ENV_STATE value (dev, prod, test).
    """

    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None
    DB_FORCE_ROLLBACK: bool = False


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    """
    Default values here can be overridden by values in the .env file:
    e.g. DB_FORCE_ROLLBACK = False in the .env file will override the value here
    The DATABASE_URL value is OK to go in the code since it does not contain any secrets (user/pwd)
    If the testing instance was a cloud db (postgres, mysql, etc) then the DATABASE_URL would be stored in the .env file
    """

    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLLBACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str) -> BaseConfig:
    """
    Returns an object of the config class based on the env_state
    """
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


config = get_config(env_state=BaseConfig().ENV_STATE)
# config.model_config.load()
# config.model_config.validate()
# config.model_config.apply()
