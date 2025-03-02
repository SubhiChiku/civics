import asyncio
import time
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from database import add_user, add_group, all_users, all_groups, remove_user
from configs import cfg

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

LOGGER_GROUP_ID = cfg.LOGGER_GROUP_ID  # Logging group for tracking

#━━━━━━━━━━━━━━━━━━━━━━━━━━ Main Process ━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(client, m: Message):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)
        await client.approve_chat_join_request(chat.id, user.id)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/free_request_accepter_bot?startgroup=true")],
            [InlineKeyboardButton("➕ Add me to your Channel ➕", url="https://t.me/free_request_accepter_bot?startchannel=true")]
        ])
        await client.send_message(
            user.id, 
            f"**Hello {user.mention}!\nWelcome to {chat.title}**",
            reply_markup=keyboard
        )
        add_user(user.id)
    except FloodWait as e:
        print(f"FloodWait error: {e}")
        await asyncio.sleep(e.value)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        remove_user(user.id)  # Remove inactive or blocked users
        print(f"User {user.id} is either deactivated, blocked, or invalid.")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def start(client, m: Message):
    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/free_request_accepter_bot?startgroup=true")],
            [InlineKeyboardButton("➕ Add me to your Channel ➕", url="https://t.me/free_request_accepter_bot?startchannel=true")]
        ])
        if m.chat.type == enums.ChatType.PRIVATE:
            await m.reply_text(
                f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve Admin Join Requests Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**",
                reply_markup=keyboard
            )
            add_user(m.from_user.id)
        elif m.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            group_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/free_request_accepter_bot?start=true")]
            ])
            await m.reply_text(
                f"**🦊 Hello {m.from_user.first_name}!\nWrite me private for more details.**",
                reply_markup=group_keyboard
            )
            add_group(m.chat.id)
        print(f"{m.from_user.first_name} has started the bot!")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback Handler ━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("button1|button2"))
async def chk(client, cb: CallbackQuery):
    try:
        bot_username = (await client.get_me()).username
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add me to your Chat ➕", url=f"https://t.me/{bot_username}?startgroup=true")]
        ])
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            await cb.message.edit(
                f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve Admin Join Requests Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            add_user(cb.from_user.id)
        print(f"{cb.from_user.first_name} interacted with the bot!")
    except Exception as e:
        print(f"Error: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━ User Statistics ━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(client, m: Message):
    user_count = len(all_users())
    group_count = len(all_groups())
    total_count = user_count + group_count
    await m.reply_text(f"""
🍀 **Chats Stats** 🍀
🙋‍♂️ Users: `{user_count}`
👥 Groups: `{group_count}`
🚧 Total users & groups: `{total_count}`
    """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("broadcast") & filters.user(cfg.SUDO))
async def broadcast(client, m: Message):
    if len(m.command) < 2:
        await m.reply("Please provide a message to broadcast.")
        return

    message_text = m.text.split(maxsplit=1)[1]
    success, fail = 0, 0
    users = all_users()
    groups = all_groups()
    
    # Sending messages to users
    for index, user_id in enumerate(users, start=1):
        try:
            await client.send_message(user_id, message_text)
            success += 1
        except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
            remove_user(user_id)  # Remove invalid users
            fail += 1
        except FloodWait as e:
            print(f"FloodWait error: Sleeping for {e.value} seconds.")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")
            fail += 1

        if index % 50 == 0:
            print("Sleeping for 10 seconds to prevent flood...")
            await asyncio.sleep(10)

    # Sending messages to groups
    for index, group_id in enumerate(groups, start=1):
        try:
            await client.send_message(group_id, message_text)
            success += 1
        except Exception as e:
            print(f"Failed to send message to group {group_id}: {e}")
            fail += 1

        if index % 50 == 0:
            print("Sleeping for 10 seconds to prevent flood...")
            await asyncio.sleep(10)

    # Sending log summary
    result_message = (
        f"📢 **Broadcast Summary**\n"
        f"✅ Success: {success}\n"
        f"❌ Failures: {fail}\n"
        f"📩 Message: {message_text}"
    )
    
    try:
        await client.send_message(LOGGER_GROUP_ID, result_message)
    except Exception as e:
        print(f"Logging failed: {e}")

    await m.reply(f"Broadcast completed.\n\n✅ Success: {success}\n❌ Failures: {fail}")

print("I'm Alive Now!")
app.run()
