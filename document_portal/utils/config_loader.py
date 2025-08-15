import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def _package_root() -> Path:
    """Returns the root directory of the package."""
    return Path(__file__).resolve().parents[1]

def load_config(item: str="", config_path: str | Path | None = None) -> dict:
    """
    Load YAML configuration as a dictionary.

    Resolution priority:
    1. Explicit `config_path` argument
    2. CONFIG_PATH environment variable
    3. <project_root>/config/config.yaml

    Raises:
        FileNotFoundError: If no config file exists at the resolved path.
        yaml.YAMLError: If the YAML file has invalid syntax.
    """
    env_config_path = os.getenv("CONFIG_PATH")
    if config_path is None:
        config_path = env_config_path or (_package_root() / "config" / "config.yaml")
    
    path = Path(config_path)
    if not path.is_absolute():
        path = _package_root() / config_path
        
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")
    
    with open(path, 'r', encoding='utf-8') as file:
        try:
            config = yaml.safe_load(file)
            return config.get(item, config) if item else config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file at {path}: {e}")