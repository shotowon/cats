from enum import Enum


class EnvConsts(str, Enum):
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'
