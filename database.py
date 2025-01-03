from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/mydatabase")  # Replace with your MongoDB URI
db = client["free_request_accepter_bot"]  # Replace with your database name
user_collection = db["users"]  # Collection name for users

def users():
    """Returns a list of user IDs stored in the database."""
    return [user["user_id"] for user in user_collection.find({}, {"_id": 0, "user_id": 1})]

def add_user(user_id):
    """Adds a new user to the database."""
    if not user_collection.find_one({"user_id": user_id}):
        user_collection.insert_one({"user_id": user_id})

def all_users():
    """Returns the total count of users."""
    return user_collection.count_documents({})

def remove_user(user_id):
    """Removes a user from the database."""
    user_collection.delete_one({"user_id": user_id})
        
