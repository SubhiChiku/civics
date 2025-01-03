from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import asyncio
from telebot import TeleBot
from bcast import send_broadcast_message
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(client, m: Message):
    op = m.chat
    user = m.from_user
    try:
        add_group(op.id)
        await client.approve_chat_join_request(op.id, user.id)
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/free_request_accepter_bot?startgroup=true"), 
                ],
                [
                    InlineKeyboardButton("➕ Add me to your Channel ➕", url="https://t.me/free_request_accepter_bot?startchannel=true")
                ]
            ]
        )
        await client.send_message(user.id, 
                                  f"**Hello {user.mention}!\nWelcome to {m.chat.title}**",
                                  reply_markup=keyboard)
        add_user(user.id)
    except FloodWait as e:
        print(f"FloodWait error: {e}")
        await asyncio.sleep(e.x)
    except InputUserDeactivated:
        print(f"User {user.id} is deactivated.")
    except UserIsBlocked:
        print(f"User {user.id} has blocked the bot.")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def start(client, m: Message):
    try:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/free_request_accepter_bot?startgroup=true"),
                ],
                [
                    InlineKeyboardButton("➕ Add me to your Channel ➕", url="https://t.me/free_request_accepter_bot?startchannel=true")
                ]
            ]
        )
        if m.chat.type == enums.ChatType.PRIVATE:
            await m.reply_text(
                f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve Admin Join Requests Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**",
                reply_markup=keyboard
            )
            add_user(m.from_user.id)
        elif m.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/free_request_accepter_bot?start=true")
                    ]
                ]
            )
            await m.reply_text(
                f"**🦊 Hello {m.from_user.first_name}!\nWrite me private for more details.**",
                reply_markup=keyboard
            )
            add_group(m.chat.id)
        print(f"{m.from_user.first_name} has started your bot!")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("button1|button2"))
async def chk(client, cb: CallbackQuery):
    try:
        bot_username = (await client.get_me()).username
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add me to your Chat ➕", url=f"https://t.me/{bot_username}?startgroup=true")
                ]
            ]
        )
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            await cb.message.edit(
                f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve Admin Join Requests Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            add_user(cb.from_user.id)
        print(f"{cb.from_user.first_name} has interacted with your bot!")
    except Exception as e:
        print(f"Error: {e}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(client, m: Message):
    user_count = all_users()
    group_count = all_groups()
    total_count = user_count + group_count
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users: `{user_count}`
👥 Groups: `{group_count}`
🚧 Total users & groups: `{total_count}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@bot.message_handler(commands=['broadcast'])
def handle_broadcast(message):
    message_text = message.text[11:]
    if message_text:
        send_broadcast_message(message_text)
        bot.reply_to(message, "Broadcast message sent to all users and groups!")
    else:
        bot.reply_to(message, "Please provide a message to broadcast.")
        
print("I'm Alive Now!")
app.run()
