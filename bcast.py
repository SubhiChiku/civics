from database import all_users, all_groups
from configs import cfg
from telebot import TeleBot

app = Client(
    "approver",
    bot_token=cfg.BOT_TOKEN)

def send_broadcast_message(message_text):
    """
    Sends a broadcast message to all users and groups.
    Logs the result of the broadcast operation.
    """
    users = get_all_users()  
    groups = get_all_groups()  
    total_sent_users = 0
    total_failed_users = 0
    total_sent_groups = 0
    total_failed_groups = 0

    for user_id in users:
        try:
            bot.send_message(user_id, message_text)
            total_sent_users += 1
            print(f"Broadcast message sent to user: {user_id}")
        except Exception as e:
            total_failed_users += 1
            print(f"Failed to send message to user {user_id}: {e}")

    for group_id in groups:
        try:
            bot.send_message(group_id, message_text)
            total_sent_groups += 1
            print(f"Broadcast message sent to group: {group_id}")
        except Exception as e:
            total_failed_groups += 1
            print(f"Failed to send message to group {group_id}: {e}")

    try:
        result_message = (
            f"Broadcast Summary:\n"
            f"Total users: {len(users)}, Sent: {total_sent_users}, Failed: {total_failed_users}\n"
            f"Total groups: {len(groups)}, Sent: {total_sent_groups}, Failed: {total_failed_groups}\n"
            f"Message: {message_text}"
        )
        bot.send_message(
            chat_id=LOGGER_GROUP_ID,
            text=result_message,
            parse_mode="HTML"
        )
        print("Broadcast message logged in logger group.")
    except Exception as e:
        print(f"Logging failed: {e}")
