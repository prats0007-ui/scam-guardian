"""Step 3: the Telegram bot. Run: python -m channels.telegram_bot"""
import asyncio

from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

import config
from graph.build import check_message


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


def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
