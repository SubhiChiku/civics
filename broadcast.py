from pyrogram import Client, filters
from database import all_users, all_groups
from configs import cfg

bot = Client("my_bot", bot_token=cfg.BOT_TOKEN)

def send_message_to_user(user_id, message):
    try:
        bot.send_message(user_id, message)
        return True
    except Exception as e:
        print(f"Failed to send to user {user_id}: {e}")
        return False

def send_message_to_group(chat_id, message):
    try:
        bot.send_message(chat_id, message)
        return True
    except Exception as e:
        print(f"Failed to send to group {chat_id}: {e}")
        return False

def broadcast_message(message):
    user_ids = [user['user_id'] for user in all_users()]
    group_ids = [group['chat_id'] for group in all_groups()]

    total_users = len(user_ids)
    total_groups = len(group_ids)
    users_sent = 0
    users_failed = 0
    groups_sent = 0
    groups_failed = 0

    for user_id in user_ids:
        if send_message_to_user(user_id, message):
            users_sent += 1
        else:
            users_failed += 1

    for chat_id in group_ids:
        if send_message_to_group(chat_id, message):
            groups_sent += 1
        else:
            groups_failed += 1

    broadcast_summary = f"""
    Broadcast Summary:
    Total users: {total_users}, Sent: {users_sent}, Failed: {users_failed}
    Total groups: {total_groups}, Sent: {groups_sent}, Failed: {groups_failed}
    """

    return broadcast_summary

@bot.on_message(filters.command("broadcast"))
def handle_broadcast(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a message to broadcast.")
        return
    broadcast_message_text = ' '.join(message.command[1:])
    summary = broadcast_message(broadcast_message_text)
    message.reply_text(summary)

bot.run()
