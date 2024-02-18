import configparser
from dataclasses import dataclass


@dataclass
class SourceConfig:
    data_dir: str


@dataclass
class TargetConfig:
    hostname: str
    port: int
    user: str
    password: str
    database: str
    schema: str
    table: str


@dataclass
class ResourceConfig:
    max_workers: int


@dataclass
class Config:
    source: SourceConfig
    target: TargetConfig
    resource: ResourceConfig


def load_config(config_file: str = "./config.ini") -> Config:
    """Loads the config from the config_file path.

    Args:
        config_file (str, optional): The config file path. Defaults to "./config.ini".

    Returns:
        Config: The config
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    app_config: Config = Config(
        source=SourceConfig(**config["Source"]),
        target=TargetConfig(**config["Target"]),
        resource=ResourceConfig(max_workers=int(config.get("Resource", "max_workers"))),
    )
    return app_config
