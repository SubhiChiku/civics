from pymongo import MongoClient

# Connect to MongoDB
MONGO_URI = "mongodb+srv://ayanosuvii0925:subhichiku123@cluster0.uw8yxkl.mongodb.net/mydatabase"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)

# Select database
db = client["free_request_accepter_bot"]  # Replace with your database name

# Collections for users and groups
user_collection = db["users"]
group_collection = db["groups"]

#━━━━━━━━━━━━━━━━━━━━━━━━━━ User Management ━━━━━━━━━━━━━━━━━━━━━━━━━━

def users():
    """Returns a list of all user IDs in the database."""
    try:
        return [user["user_id"] for user in user_collection.find({}, {"_id": 0, "user_id": 1})]
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def add_user(user_id):
    """Adds a new user to the database if not already present."""
    try:
        user_collection.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    except Exception as e:
        print(f"Error adding user {user_id}: {e}")

def all_users():
    """Returns the total count of users."""
    try:
        return user_collection.count_documents({})
    except Exception as e:
        print(f"Error counting users: {e}")
        return 0

def remove_user(user_id):
    """Removes a user from the database."""
    try:
        user_collection.delete_one({"user_id": user_id})
    except Exception as e:
        print(f"Error removing user {user_id}: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━ Group Management ━━━━━━━━━━━━━━━━━━━━━━━━━━

def groups():
    """Returns a list of all group IDs in the database."""
    try:
        return [group["group_id"] for group in group_collection.find({}, {"_id": 0, "group_id": 1})]
    except Exception as e:
        print(f"Error fetching groups: {e}")
        return []

def add_group(group_id):
    """Adds a new group to the database if not already present."""
    try:
        group_collection.update_one({"group_id": group_id}, {"$set": {"group_id": group_id}}, upsert=True)
    except Exception as e:
        print(f"Error adding group {group_id}: {e}")

def all_groups():
    """Returns the total count of groups."""
    try:
        return group_collection.count_documents({})
    except Exception as e:
        print(f"Error counting groups: {e}")
        return 0

def remove_group(group_id):
    """Removes a group from the database."""
    try:
        group_collection.delete_one({"group_id": group_id})
    except Exception as e:
        print(f"Error removing group {group_id}: {e}")
