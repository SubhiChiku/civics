import os

class Config:
    API_ID = int(os.getenv("API_ID", "21189715"))  
    API_HASH = os.getenv("API_HASH", "988a9111105fd2f0c5e21c2c2449edfd")  
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7485296857:AAEpfLsEF48O_-8iepYVI_wp2zhVMXaQLR4")  
    SUDO = list(map(int, filter(None, os.getenv("SUDO", "7225660023").replace(" ", "").split(","))))  
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/mydatabase")  
    LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID", "-1002341427688"))  

cfg = Config()
