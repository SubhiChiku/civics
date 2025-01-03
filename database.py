from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/mydatabase")  # Replace with your MongoDB URI
db = client["free_request_accepter_bot"]  # Replace with your database name
db = client["main"]
# Collections for users and groups
user_collection = db["users"]  # Collection for users
group_collection = db["groups"]  # Collection for groups

# User Management
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

# Group Management
def groups():
    """Returns a list of group IDs stored in the database."""
    return [group["group_id"] for group in group_collection.find({}, {"_id": 0, "group_id": 1})]

def add_group(group_id):
    """Adds a new group to the database."""
    if not group_collection.find_one({"group_id": group_id}):
        group_collection.insert_one({"group_id": group_id})

def all_groups():
    """Returns the total count of groups."""
    return group_collection.count_documents({})

def remove_group(group_id):
    """Removes a group from the database."""
    group_collection.delete_one({"group_id": group_id})
