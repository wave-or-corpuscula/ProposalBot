import yaml

import logging.config


with open("logging_config.yaml", "r") as file:
    config = yaml.safe_load(file)

logging.config.dictConfig(config)
logger = logging.getLogger("main_bot_logger")