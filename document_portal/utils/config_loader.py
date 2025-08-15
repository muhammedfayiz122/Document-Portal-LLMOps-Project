import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

# Absolute path to the package root directory
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Absolute path to the top-level project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Absolute path to the config directory
CONFIG_PATH = PACKAGE_ROOT / "config" / "config.yaml"

# Loading environment variables from .env file if it exists
env_path = PROJECT_ROOT.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

def get_project_root() -> Path:
    """Returns the root directory of the project."""
    return PROJECT_ROOT

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
        config_path = env_config_path or str(CONFIG_PATH)
    
    config_path = Path(config_path)
    if not config_path.is_absolute():
        config_path = PACKAGE_ROOT / config_path
        
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as file:
        try:
            config = yaml.safe_load(file)
            return config.get(item, config) if item else config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file at {config_path}: {e}")