# bot.py - Main command handlers
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from database import db
import logging

# Initialize logger
logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command with welcome message"""
    try:
        # Check if user exists in DB
        if not await db.users.get_user(message.from_user.id):
            await db.users.create_user(message.from_user.id, message.from_user.first_name)
            
        # Create buttons
        buttons = [
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("🔑 Login", callback_data="login")],
            [InlineKeyboardButton("📢 Updates", url="https://t.me/vj_botz"),
             InlineKeyboardButton("💬 Support", url="https://t.me/vj_bot_disscussion")]
        ]
        
        await message.reply_text(
            f"👋 Hello {message.from_user.mention}!\n\n"
            "I can help you download restricted content from Telegram.\n\n"
            "🔐 Use /login to start session\n"
            "🆘 Use /help for usage guide",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
    except Exception as e:
        logger.error(f"Start command error: {str(e)}")
        await message.reply_text("❌ Failed to process command")

@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command with usage instructions"""
    help_text = (
        "📖 **Usage Guide**\n\n"
        "1. For public content:\n"
        "   `https://t.me/channel/123`\n\n"
        "2. For private content:\n"
        "   First send chat invite link\n"
        "   Then send post link\n\n"
        "3. For multiple posts:\n"
        "   `https://t.me/channel/100-120`\n\n"
        "4. Commands:\n"
        "   /login - Start session\n"
        "   /logout - End session\n"
        "   /cancel - Stop current operation"
    )
    await message.reply_text(help_text)

@Client.on_message(filters.command("login") & filters.private)
async def login_command(client: Client, message: Message):
    """Handle login flow"""
    try:
        # Step 1: Request phone number
        sent_msg = await message.reply_text(
            "📱 Please send your phone number in international format:\n"
            "Example: `+1234567890`\n\n"
            "Type /cancel to abort"
        )
        
        # Step 2: Wait for phone number input
        phone_msg = await client.listen(
            chat_id=message.chat.id,
            filters=filters.text & filters.private,
            timeout=300
        )
        
        if phone_msg.text.lower() == "/cancel":
            return await message.reply_text("❌ Login cancelled")
            
        # Step 3: Send OTP
        sent_code = await client.send_code(phone_msg.text)
        
        # Step 4: Request OTP
        await message.reply_text(
            "🔢 Enter the OTP received in format: `1 2 3 4 5`\n\n"
            "Type /cancel to abort"
        )
        
        # Step 5: Wait for OTP input
        otp_msg = await client.listen(
            chat_id=message.chat.id,
            filters=filters.text & filters.private,
            timeout=300
        )
        
        if otp_msg.text.lower() == "/cancel":
            return await message.reply_text("❌ Login cancelled")
            
        # Step 6: Complete login
        await client.sign_in(
            phone_number=phone_msg.text,
            phone_code_hash=sent_code.phone_code_hash,
            phone_code=otp_msg.text.replace(" ", "")
        )
        
        # Step 7: Save session
        session_string = await client.export_session_string()
        await db.users.update_session(message.from_user.id, session_string)
        
        await message.reply_text("✅ Login successful!")
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        await message.reply_text("❌ Login failed. Please try /login again")

@Client.on_message(filters.command("logout") & filters.private)
async def logout_command(client: Client, message: Message):
    """Handle logout command"""
    try:
        await db.users.update_session(message.from_user.id, None)
        await message.reply_text("✅ Logout successful!")
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        await message.reply_text("❌ Logout failed")

@Client.on_message(filters.command("cancel") & filters.private)
async def cancel_command(client: Client, message: Message):
    """Handle operation cancellation"""
    try:
        # Add cancellation logic for current operations
        await message.reply_text("🚫 Current operation cancelled")
    except Exception as e:
        logger.error(f"Cancel error: {str(e)}")
        await message.reply_text("❌ Failed to cancel operation")

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS))
async def broadcast_command(client: Client, message: Message):
    """Admin broadcast handler"""
    try:
        if not message.reply_to_message:
            return await message.reply_text("❌ Reply to a message to broadcast")
            
        users = await db.users.get_all_users()
        success = 0
        failed = 0
        
        for user in users:
            try:
                await client.copy_message(
                    chat_id=user['user_id'],
                    from_chat_id=message.chat.id,
                    message_id=message.reply_to_message.id
                )
                success += 1
            except Exception:
                failed += 1
                
        await message.reply_text(
            f"📢 Broadcast complete!\n\n"
            f"✅ Success: {success}\n"
            f"❌ Failed: {failed}"
        )
        
    except Exception as e:
        logger.error(f"Broadcast error: {str(e)}")
        await message.reply_text("❌ Broadcast failed")
