from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import asyncio

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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(client, m: Message):
    all_users_data = users
    response_message = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    
    for user_record in all_users_data.find():
        try:
            user_id = user_record["user_id"]
            await m.reply_to_message.forward(int(user_id))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.x)
            await m.reply_to_message.forward(int(user_id))
        except InputUserDeactivated:
            deactivated += 1
            remove_user(user_id)
        except UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(f"Error: {e}")
            failed += 1

    await response_message.edit(
        f"✅ Successfully forwarded to `{success}` users.\n❌ Failed for `{failed}` users.\n👾 Found `{blocked}` blocked users.\n👻 Found `{deactivated}` deactivated users."
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Accept Pending Requests on Startup ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start") & filters.user(cfg.SUDO))
async def accept_pending_requests(client, m: Message):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            try:
                pending_requests = await client.get_chat_join_requests(dialog.chat.id)
                for request in pending_requests:
                    await client.approve_chat_join_request(dialog.chat.id, request.user.id)
                    await client.send_message(request.user.id, f"**Hello {request.user.mention}!\nWelcome to {dialog.chat.title}**")
                    add_user(request.user.id)
                    add_group(dialog.chat.id)
            except Exception as e:
                print(f"Error while processing pending requests for {dialog.chat.title}: {e}")

print("I'm Alive Now!")
app.run()
