from document_portal.utils.config_loader import load_config

config = load_config("cloud_logger")
print(config["file_handler"]['level'])