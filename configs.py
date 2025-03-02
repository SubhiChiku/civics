import os

class Config:
    API_ID = int(os.getenv("API_ID", "0"))  # Default to 0 if not set
    API_HASH = os.getenv("API_HASH", "")  # Empty string as default
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # Empty string as default
    SUDO = list(map(int, filter(None, os.getenv("SUDO", "").replace(" ", "").split(","))))  # Removes spaces and handles empty case
    MONGO_URI = os.getenv("MONGO_URI", "")
    LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID", "-1000000000000"))  # Default to a valid Telegram group ID

cfg = Config()
