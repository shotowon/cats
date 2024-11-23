import logging
from cats.gears.config import EnvConsts


def configure_logging(env: EnvConsts):
    """
    Configures logging based on the provided environment.

    This function sets up logging behavior based on the `env` argument,
    which should be one of the `EnvConsts` values.
    The logging configuration includes setting log levels,
    formatting log messages, and configuring log handlers
    to output to either the console or log files.

    - For `EnvConsts.LOCAL`:
        Logs are output to the console with DEBUG level.
    - For `EnvConsts.DEV`:
        Logs are output both to the console and
        to a log file ('logs/cats.dev.log') with INFO level.
        Console logs are in a simple format,
        while file logs are in JSON-like format.
    - For `EnvConsts.PROD`:
        Logs are output to a log file ('logs/cats.prod.log')
        with INFO level in JSON-like format.

    Args:
        env (EnvConsts): The environment constant used to determine the
            logging configuration. Must be one of `EnvConsts.LOCAL`,
            `EnvConsts.DEV`, or `EnvConsts.PROD`.

    Raises:
        ValueError: If the provided `env` value is not valid.
    """
    if env == EnvConsts.LOCAL:
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
                level=logging.DEBUG,
                format=fmt,
                )
        logging.root.name = f'cats | {env.value}'
    elif env == EnvConsts.DEV:
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('logs/cats.dev.log')
        stream_fmt = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
        file_fmt = logging.Formatter(
                """{
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level"": "%(levelname)s",
    "message": "%(message)s"
}"""
                )
        stream_handler.setFormatter(stream_fmt)
        file_handler.setFormatter(file_fmt)

        logging.root.setLevel(logging.INFO)
        logging.root.addHandler(stream_handler)
        logging.root.addHandler(file_handler)
        logging.root.name = f'cats - {env.value}'
    elif env == EnvConsts.PROD:
        file_handler = logging.FileHandler('logs/cats.prod.log')
        file_fmt = logging.Formatter(
                """{
    "time": "%(asctime)s",
    "name": "%(name)s",
    "level"": "%(levelname)s",
    "message": "%(message)s"
}"""
                )
        file_handler.setFormatter(file_fmt)

        logging.root.setLevel(logging.INFO)
        logging.root.addHandler(file_handler)
        logging.root.name = f'cats - {env.value}'
    else:
        raise ValueError(f'log: invalid env var: {env}')
