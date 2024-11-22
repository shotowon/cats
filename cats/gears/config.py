from enum import Enum
from pydantic import BaseModel, Field


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
