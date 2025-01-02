from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
import asyncio

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(client, m: Message):
    try:
        # Ensure the database collection is queried correctly
        all_users_data = list(users.find())
        user_count = len(all_users_data)
        print(f"Found {user_count} users.")
        
        if user_count == 0:
            await m.reply_text("No users found to broadcast.")
            return
        
        if not m.reply_to_message:
            await m.reply_text("Reply to a message to broadcast.")
            return

        response_message = await m.reply_text("`⚡️ Processing broadcast...`")
        success, failed, deactivated, blocked = 0, 0, 0, 0

        for user_record in all_users_data:
            try:
                user_id = int(user_record["user_id"])
                await m.reply_to_message.copy(user_id)
                success += 1
                print(f"Successfully sent to {user_id}")
            
            except FloodWait as ex:
                print(f"FloodWait: Waiting for {ex.x} seconds")
                await asyncio.sleep(ex.x)
            
            except InputUserDeactivated:
                print(f"User {user_id} deactivated.")
                deactivated += 1
                remove_user(user_id)  # Ensure this function is defined
            
            except UserIsBlocked:
                print(f"User {user_id} blocked the bot.")
                blocked += 1
            
            except Exception as e:
                print(f"Broadcast failed for {user_id}: {e}")
                failed += 1

        # Edit the response message with summary
        await response_message.edit(
            f"✅ Successfully sent to `{success}` users.\n"
            f"❌ Failed for `{failed}` users.\n"
            f"👾 Blocked: `{blocked}` users.\n"
            f"👻 Deactivated: `{deactivated}` users."
        )
    
    except Exception as e:
        await m.reply_text(f"Error in broadcast: {e}")
        print(f"Error in broadcast: {e}")
