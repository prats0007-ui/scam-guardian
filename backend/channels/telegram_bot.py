"""Step 3: the Telegram bot. Run: python -m channels.telegram_bot"""
import asyncio
import time
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

import config
from graph.build import check_message
from llm import read_image


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm Scam Guardian 🛡️\nForward me any suspicious message and I'll check it for you."
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption
    if not text:
        await update.message.reply_text("For now, please send the message as text. Screenshots are coming soon!")
        return
    await update.message.reply_text("🔍 Investigating…")
    try:
        reply = await asyncio.to_thread(check_message, text)
    except Exception as e:
        print("Error:", e)
        reply = "Sorry, something went wrong. Please try again in a minute."
    await update.message.reply_text(reply, disable_web_page_preview=True)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not config.MODEL_VISION:
        await update.message.reply_text("Screenshot checks aren't set up yet. Please send the message as text.")
        return
    await update.message.reply_text("📸 Reading your screenshot…")
    try:
        photo = update.message.photo[-1]  # Telegram sends several sizes; the last is the largest
        file = await photo.get_file()
        image_bytes = bytes(await file.download_as_bytearray())
        start = time.perf_counter()
        text = await asyncio.to_thread(read_image, image_bytes)
        print(f"⏱ read_image: {time.perf_counter() - start:.1f}s")
        if not text or text == "NO_TEXT":
            await update.message.reply_text(
                "I couldn't find any text in that image. Try a clearer screenshot, or send the message as text."
            )
            return
        if update.message.caption:
            text = f"{text}\n\n(Note from user: {update.message.caption})"
        await update.message.reply_text("🔍 Investigating…")
        reply = await asyncio.to_thread(check_message, text)
    except Exception as e:
        print("Error:", e)
        reply = "Sorry, something went wrong. Please try again in a minute."
    await update.message.reply_text(reply, disable_web_page_preview=True)

def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
