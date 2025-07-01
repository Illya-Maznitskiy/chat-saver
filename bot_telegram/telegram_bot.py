from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

from selenium_scraper.scraper import scrape_quotes
from logs.logger import logger


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ERROR_MSG = "Oops, something went wrong."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /start command: greet user.
    """
    try:
        logger.info(f"User {update.effective_user.id} used /start")
        await update.message.reply_text(
            "👋 Hello! I'm your bot. Use /run to get quotes."
        )
    except Exception as e:
        logger.error(f"Error in /start handler: {e}")
        await update.message.reply_text(ERROR_MSG)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /about command: send bot info.
    """
    try:
        logger.info(f"User {update.effective_user.id} used /about")
        await update.message.reply_text(
            "🤖 This bot sends quotes via Telegram and runs a scraper."
        )
    except Exception as e:
        logger.error(f"Error in /about handler: {e}")
        await update.message.reply_text(ERROR_MSG)


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /run command: run scraper and send quotes.
    """
    try:
        logger.info(f"User {update.effective_user.id} started scraping")
        await update.message.reply_text("⚙️ Running scraper...")
        quotes = scrape_quotes()
        await update.message.reply_text(quotes)
    except Exception as e:
        logger.error(f"Error in /run handler: {e}")
        await update.message.reply_text(ERROR_MSG)


def run_bot():
    """
    Start the Telegram bot and register command handlers.
    """
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in environment variables!")
        return

    logger.info("Starting Telegram bot")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("run", run))

    app.run_polling()
