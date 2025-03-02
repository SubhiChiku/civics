import time
from database import all_users, all_groups
from configs import cfg
from telebot import TeleBot

app = TeleBot(cfg.BOT_TOKEN)
LOGGER_GROUP_ID = cfg.LOGGER_GROUP_ID  # Ensure this exists in your configs


def send_broadcast_message(message_text):
    """
    Sends a broadcast message to all users and groups.
    Introduces a sleep timer of 10 seconds after sending messages to every 50 users/groups.
    Logs the result of the broadcast operation.
    """
    users = all_users()  
    groups = all_groups()  
    total_sent_users = 0
    total_failed_users = 0
    total_sent_groups = 0
    total_failed_groups = 0

    # Sending messages to users
    for index, user_id in enumerate(users, start=1):
        try:
            app.send_message(user_id, message_text)
            total_sent_users += 1
            print(f"Broadcast message sent to user: {user_id}")
        except Exception as e:
            total_failed_users += 1
            print(f"Failed to send message to user {user_id}: {e}")

        if index % 50 == 0:  # Pause every 50 messages
            print("Sleeping for 10 seconds to prevent flood...")
            time.sleep(10)

    # Sending messages to groups
    for index, group_id in enumerate(groups, start=1):
        try:
            app.send_message(group_id, message_text)
            total_sent_groups += 1
            print(f"Broadcast message sent to group: {group_id}")
        except Exception as e:
            total_failed_groups += 1
            print(f"Failed to send message to group {group_id}: {e}")

        if index % 50 == 0:  # Pause every 50 messages
            print("Sleeping for 10 seconds to prevent flood...")
            time.sleep(10)

    # Logging the broadcast result
    try:
        result_message = (
            f"<b>Broadcast Summary:</b>\n"
            f"Total users: {len(users)}, Sent: {total_sent_users}, Failed: {total_failed_users}\n"
            f"Total groups: {len(groups)}, Sent: {total_sent_groups}, Failed: {total_failed_groups}\n"
            f"<b>Message:</b> {message_text}"
        )
        app.send_message(
            chat_id=LOGGER_GROUP_ID,
            text=result_message,
            parse_mode="HTML"
        )
        print("Broadcast message logged in logger group.")
    except Exception as e:
        print(f"Logging failed: {e}")
