from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

BOT_TOKEN = "7815909620:AAEZi0vd6oCNAYQeM8VesNFQfj_waYXh68k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"Chat ID kamu: {chat_id}")
    print(type(chat_id))
    await update.message.reply_text("Hello🤖 Kirimkan Review, Saya akan analisis sentimennya")

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     prediction = "POSITIF"
#     print("Pesan")
#     await update.message.reply_text(f"Prediksi sentimen: {prediction}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

run_bot()
