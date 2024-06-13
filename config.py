import json
import os

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), r"data\config.json")
# os.path.join(os.path.dirname(__file__), r"\data\config.json")

TEXT_ARRAY_SIZE = "TextArraySize"
RETURNED_LIMIT = "ReturnedLimit"

CONFIG_VALUES = {
    TEXT_ARRAY_SIZE: {
        "default": 100,
        "type": int,
    },
    RETURNED_LIMIT: {"default": 10, "type": int},
}

with open(CONFIG_FILE_PATH, encoding="utf-8") as config_file:
    jsonvalues = json.load(config_file)

CONFIG_VALUES = jsonvalues
