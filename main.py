import threading

from bot_whatsapp.whatsapp_handler import run_whatsapp_bot
from bot_telegram.telegram_bot import run_bot
from logs.logger import logger


def main():
    """
    Starts the WhatsApp bot in a separate thread
    and runs the Telegram bot in the main thread.
    """
    # Run WhatsApp bot in a separate thread
    logger.info("Starting WhatsApp bot thread...")
    whatsapp_thread = threading.Thread(target=run_whatsapp_bot)
    whatsapp_thread.start()

    # Run Telegram bot in the main thread
    logger.info("Running Telegram bot thread...")
    run_bot()


if __name__ == "__main__":
    main()
