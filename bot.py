from pyrogram import Client, filters, enums, errors
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.flood_420 import FloodWait
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

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    user = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, user.id)
        await app.send_message(user.id, f"**Hello {user.mention}!\nWelcome to {m.chat.title}\n\n__Powered By: @sifrapprovalbot__**")
        add_user(user.id)
    except errors.PeerIdInvalid:
        print("User isn't started the bot (means group).")
    except Exception as err:
        print(str(err))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="tg://settings"),
                        InlineKeyboardButton("💬 Support", url="tg://settings")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/?startgroup")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_text("**🦊 Hello {}!\nI'm an auto-approve [Admin Join Requests](tg://settings) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**".format(m.from_user.mention), reply_markup=keyboard)
    
        elif m.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/{app.username}?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**🦊 Hello {}!\nWrite me private for more details.**".format(m.from_user.first_name), reply_markup=keyboard)
        print(m.from_user.first_name + " has started your bot!")

    except Exception as err:
        print(str(err))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="tg://settings"),
                        InlineKeyboardButton("💬 Support", url="tg://settings")
                    ],
                    [
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/{app.username}?startgroup=true")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**🦊 Hello {}!\nI'm an auto-approve [Admin Join Requests](tg://settings) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.**".format(cb.from_user.mention), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name + " has started your bot!")
    except Exception as e:
        print(str(e))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    user_count = all_users()
    group_count = all_groups()
    total_count = user_count + group_count
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users: `{user_count}`
👥 Groups: `{group_count}`
🚧 Total users & groups: `{total_count}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    all_users = users
    response_message = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for user_record in all_users.find():
        try:
            user_id = user_record["user_id"]
            await m.reply_to_message.copy(int(user_id))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(user_id))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(user_id)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await response_message.edit(f"✅ Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    all_users = users
    response_message = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for user_record in all_users.find():
        try:
            user_id = user_record["user_id"]
            await m.reply_to_message.forward(int(user_id))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(user_id))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(user_id)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await response_message.edit(f"✅ Successful to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
