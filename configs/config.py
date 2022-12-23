from modules import Json
from os.path import isfile
from datetime import timedelta, timezone, time
from logging import getLevelName
from typing import Union

# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG
# NOTSET

class LoggingConfig:
    STREAM_LEVEL: int = 20
    FILE_LEVEL: int = 20
    BACKUP_COUNT: int
    FILE_NAME: str
    DIR_PATH: str
    def __init__(self, data: dict) -> None:
        if type(getLevelName(data["stream_level"])) == int:
            self.STREAM_LEVEL = data["stream_level"]
        if type(getLevelName(data["file_level"])) == int:
            self.FILE_LEVEL = data["file_level"]
        self.BACKUP_COUNT = abs(data["backup_count"])
        self.FILE_NAME = data["file_name"]
        self.DIR_PATH = data["dir_path"]

CONFIG = {
    "discord": {
        "token": "",
        "channel_id": 0,
        "prefixs": ["$"]
    },
    "logging": {
        "main": {
            "stream_level": "INFO",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "main",
            "dir_path": "logs",
        },
        "discord": {
            "stream_level": "WARNING",
            "file_level": "INFO",
            "backup_count": 3,
            "file_name": "discord",
            "dir_path": "logs",
        },
    },
    "timezone": 8,
}

try:
    RAW_CONFIG: dict[str, Union[dict, str, int]] = Json.load("config.json")
    for key, value in RAW_CONFIG.items():
        if type(value) == dict:
            for s_key, s_value in value.items():
                CONFIG[key][s_key] = s_value
        else:
            CONFIG[key] = value
    Json.dump("config.json", CONFIG)
except Exception as e:
    input("未檢測到 config.json，已重新生成，請前往修改。")
    Json.dump("config.json", CONFIG)
    raise e
    

DISCORD_TOKEN: str = CONFIG["discord"]["token"]
DISCORD_CHANNEL: int = CONFIG["discord"]["channel_id"]
DISCORD_PREFIXS: tuple[str] = tuple(CONFIG["discord"]["prefixs"])

LOGGING_CONFIG: dict[str, LoggingConfig] = {
    "main": LoggingConfig(CONFIG["logging"]["main"]),
    "discord": LoggingConfig(CONFIG["logging"]["discord"]),
}

TIMEZONE: timezone = timezone(timedelta(hours=CONFIG["timezone"]))
        