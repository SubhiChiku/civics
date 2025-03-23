import time
import logging
from database import all_users, all_groups
from configs import cfg
from telebot import TeleBot

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = TeleBot(cfg.BOT_TOKEN)
LOGGER_GROUP_ID = cfg.LOGGER_GROUP_ID  # Ensure this is correctly set in configs


def send_message(receiver_id, message_text):
    """
    Sends a message to a given user or group.
    Handles exceptions to log errors.
    """
    try:
        app.send_message(receiver_id, message_text)
        logging.info(f"Broadcast message sent to {receiver_id}")
        return True
    except Exception as e:
        logging.error(f"Failed to send message to {receiver_id}: {e}")
        return False


def send_broadcast_message(message_text):
    """
    Sends a broadcast message to all users and groups.
    Introduces a 10-second sleep timer after sending messages to every 50 users/groups.
    Logs the results in the logger group.
    """
    users = all_users()
    groups = all_groups()
    total_sent_users, total_failed_users = 0, 0
    total_sent_groups, total_failed_groups = 0, 0

    def process_recipients(recipients, entity_type):
        """
        Helper function to process message sending to users or groups.
        It sleeps for 10 seconds after every 50 messages.
        """
        nonlocal total_sent_users, total_failed_users, total_sent_groups, total_failed_groups
        
        for index, recipient_id in enumerate(recipients, start=1):
            success = send_message(recipient_id, message_text)
            
            if entity_type == "user":
                if success:
                    total_sent_users += 1
                else:
                    total_failed_users += 1
            else:  # entity_type == "group"
                if success:
                    total_sent_groups += 1
                else:
                    total_failed_groups += 1

            # Sleep every 50 messages to avoid flooding
            if index % 50 == 0:
                logging.info("Sleeping for 10 seconds to prevent flood...")
                time.sleep(10)

    # Process users
    logging.info("Starting broadcast to users...")
    process_recipients(users, "user")

    # Process groups
    logging.info("Starting broadcast to groups...")
    process_recipients(groups, "group")

    # Logging the broadcast result in logger group
    try:
        result_message = (
            f"<b>📢 Broadcast Summary:</b>\n"
            f"👤 Users - Total: {len(users)}, ✅ Sent: {total_sent_users}, ❌ Failed: {total_failed_users}\n"
            f"👥 Groups - Total: {len(groups)}, ✅ Sent: {total_sent_groups}, ❌ Failed: {total_failed_groups}\n"
            f"<b>📨 Message:</b> {message_text}"
        )
        app.send_message(
            chat_id=LOGGER_GROUP_ID,
            text=result_message,
            parse_mode="HTML"
        )
        logging.info("Broadcast summary sent to logger group.")
    except Exception as e:
        logging.error(f"Failed to log broadcast summary: {e}")


# Example usage:
if __name__ == "__main__":
    message = "🚀 This is a test broadcast message. Stay tuned for updates!"
    send_broadcast_message(message)
