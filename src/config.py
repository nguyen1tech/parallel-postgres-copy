import configparser
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    hostname: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class SourceConfig:
    data_dir: str


@dataclass
class TargetConfig:
    schema: str
    table: str


@dataclass
class ResourceConfig:
    max_workers: int


@dataclass
class Config:
    database: DatabaseConfig
    source: SourceConfig
    target: TargetConfig
    resource: ResourceConfig


def load_config(config_file: str = "./config.ini") -> Config:
    config = configparser.ConfigParser()
    config.read(config_file)

    app_config: Config = Config(
        database=DatabaseConfig(**config["Database"]),
        source=SourceConfig(**config["Source"]),
        target=TargetConfig(**config["Target"]),
        resource=ResourceConfig(max_workers=int(config.get("Resource", "max_workers"))),
    )
    return app_config
