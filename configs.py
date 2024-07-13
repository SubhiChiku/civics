from os import getenv

class Config:
    API_ID = int(getenv("API_ID", "21189715"))
    API_HASH = getenv("API_HASH", "988a9111105fd2f0c5e21c2c2449edfd")
    BOT_TOKEN = getenv("BOT_TOKEN", "7485296857:AAEL_5uTPiaPbIt9iNmAhv96OWHV6ObE1J4)
    CHID = int(getenv("CHID", "-1002152429971"))
    SUDO = list(map(int, getenv("SUDO", "6798912985").split(",")))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

cfg = Config()
