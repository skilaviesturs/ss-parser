import asyncio
import signal
import platform
import contextlib
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from lib.logger import logger
from lib.parser_main import run_parser
from lib.notifier_telegram import set_telegram_context
from lib.handle_help import handle_help
from lib.handle_monitor_callback import handle_monitor_callback
from lib.handle_monitor_list import handle_monitor_list
from lib.handle_unmonitor_callback import handle_unmonitor_callback
from lib.config import PARSE_INTERVAL_MINUTES, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

stop_event = asyncio.Event()

def handle_signal():
    logger.info("[main] 🚦 SIGINT/SIGTERM received, shutting down...")
    stop_event.set()

async def parser_loop():
    while not stop_event.is_set():
        logger.info("[main] Running parser...")
        try:
            await run_parser()
        except Exception as e:
            logger.error(f"[runner] Parser crashed: {str(e)}")
        logger.info(f"[main] Sleeping for {PARSE_INTERVAL_MINUTES} minutes...")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=PARSE_INTERVAL_MINUTES * 60)
        except asyncio.TimeoutError:
            pass

async def wait_for_keyboard_interrupt():
    try:
        await asyncio.Event().wait()  # endless wait
    except asyncio.CancelledError:
        pass  # expected on shutdown

async def async_main():
    loop = asyncio.get_running_loop()
    tasks = [asyncio.create_task(parser_loop())]

    if platform.system() != "Windows":
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, handle_signal)
    else:
        # On Windows, simulate with background task
        task = asyncio.create_task(wait_for_keyboard_interrupt())
        tasks.append(task)

    telegram_app = None

    try:
        if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
            telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
            set_telegram_context(telegram_app.bot, telegram_app)
            telegram_app.add_handler(CommandHandler("help", handle_help))
            telegram_app.add_handler(CallbackQueryHandler(handle_monitor_callback, pattern=r"^monitor:"))
            telegram_app.add_handler(CommandHandler("list", handle_monitor_list))
            telegram_app.add_handler(CallbackQueryHandler(handle_unmonitor_callback, pattern=r"^unmonitor:"))
            logger.info("[bot] ✅ Telegram bot initialized, command and callback handlers registered.")

            await telegram_app.initialize()
            await telegram_app.start()
            tasks.append(asyncio.create_task(telegram_app.updater.start_polling()))

        await stop_event.wait()

    finally:
        logger.info("[main] ⏹ Shutting down all tasks...")

        for task in tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        if telegram_app:
            await telegram_app.updater.stop()
            await telegram_app.stop()
            await telegram_app.shutdown()

        logger.info("[main] ✅ Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("[main] ⌨️ KeyboardInterrupt received. Shutting down.")
