import argparse
import os
import yaml
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field

CFG_PATH_ENV_VAR = 'CATS_CONFIG_PATH'


class ConfigPathNotSetError(Exception):
    pass


class EnvConsts(str, Enum):
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'


class HTTPServerConfig(BaseModel):
    host: str = Field(default='127.0.0.1')
    port: int = Field(default=6810)


class Config(BaseModel):
    env: EnvConsts
    storage_name: str = Field(default='storage/local.db')
    http_server: HTTPServerConfig


def load_config() -> Config:
    """ Loads 'cats' configuration.

    Returns:
        Config: object with all values needed for configuration
    Raises:
        ConfigPathNotSetError: If the '--config' argument and
            environment variable in CFG_PATH_ENV_VAR is not set.
        FileNotFoundError: If config file not found.
        yaml.YAMLError: If yaml.safe_load failed
            to parse contents of config file.
    """
    parser = argparse.ArgumentParser(description='load config file')
    parser.add_argument(
            '--config',
            type=str,
            help='path to the config file'
            )
    args = parser.parse_args()

    cfg_path = args.config.strip() if args.config else ''
    if cfg_path == '':
        cfg_path = os.getenv(CFG_PATH_ENV_VAR, '')

    if cfg_path == '':
        raise ConfigPathNotSetError(
                f'config: {CFG_PATH_ENV_VAR} env variable is not set'
                )

    try:
        return Config(**yaml.safe_load(Path(cfg_path).read_text()))
    except FileNotFoundError as error:
        raise FileNotFoundError(f'config: config file not found: {error}')
    except yaml.YAMLError as error:
        raise yaml.YAMLError(
                f'config: failed to parse yaml of config file {error}'
                )
