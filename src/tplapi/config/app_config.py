import os
import shutil
from importlib import resources
from pathlib import Path

import yaml
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    upload_dir: str
    nmparse_url: str


def load_config():
    config_dict = {}
    yaml_config = os.environ.get("TEMPLATES_API_CONFIG")
    if yaml_config is None:
        config_path = resources.as_file(
            resources.files("tplapi.config").joinpath("config.yaml")
        )
        with config_path as p:
            with p.open() as f:
                config_dict = yaml.safe_load(f)
    else:
        with open(yaml_config, "r") as config_file:
            config_dict = yaml.safe_load(config_file)
    return AppConfig(**config_dict)


def migrate_dir(UPLOAD_DIR, NEXUS_DIR):
    for filename in Path(UPLOAD_DIR).glob("*.nxs"):
        shutil.move(filename, NEXUS_DIR)


def initialize_dirs(migrate=False):
    config = load_config()
    UPLOAD_DIR = config.upload_dir
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    NEXUS_DIR = os.path.join(UPLOAD_DIR, "NEXUS")
    os.makedirs(NEXUS_DIR, exist_ok=True)
    TEMPLATE_DIR = os.path.join(UPLOAD_DIR, "TEMPLATES")
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    if migrate:
        migrate_dir(UPLOAD_DIR, NEXUS_DIR)
    return config, UPLOAD_DIR, NEXUS_DIR, TEMPLATE_DIR
