import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from src.translator import translate
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def translate_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    message = update.message
    if message.from_user.is_bot:
        return
    if update.message.chat.type == "private":
        return
    if "[no translate]" in message.text:
        return
    text = message.text or ""
    try:
        translated = translate(text)
        await message.reply_text(text=translated)
    except Exception as e:
        print(f"[ERR] translating message: {e}")


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_handler))
    while True:
        try:
            print("[OK] bot init.")
            app.run_polling()
        except Exception as e:
            print(f"[WARN] {str(e)[:50]}.\n[WAIT] restarting in 5s.")
            time.sleep(5)


if __name__ == "__main__":
    main()
