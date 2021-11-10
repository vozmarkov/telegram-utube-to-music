from __future__ import unicode_literals
import logging
import os
import youtube_dl
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def error(update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Something went wrong, please try again later!"
    )


def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False


def download_utube(update, context: CallbackContext):
    url = update.message.text
    if is_supported(url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0]+".mp3"
        context.bot.send_audio(
            chat_id=update.effective_chat.id, audio=open(filename, 'rb'))
        context.bot.delete_message(
            chat_id=update.message.chat.id, message_id=update.message.message_id)
    try:
        os.remove(filename)
    except OSError:
        pass


def help_command(update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Simple Bot, paste youtube vid url and wait for bot to respond with mp3, in order for bot to delete url message it needs admin permissions"
    )


def start_command(update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, simple bot created to paste youtube url and it will convert into mp3 and send it back to chat, also will delete the message with url, thanks"
    )


def main():
    # Load .env variables
    if os.getenv("telegram_key") is None:
        import dotenv
        dotenv.load_dotenv()
    # telegram bot setup
    updater = Updater(token=os.getenv('telegram_key'),
                      use_context=True, workers=30)
    dispatcher = updater.dispatcher

    # logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # default handlers
    start_handler = CommandHandler("start", start_command)
    dispatcher.add_handler(start_handler)
    help_handler = CommandHandler("help", help_command)
    dispatcher.add_handler(help_handler)

    # youtube download and covert to mp3 handler
    utubeUrl_handler = MessageHandler(
        Filters.text, download_utube, run_async=30)
    dispatcher.add_handler(utubeUrl_handler)

    # Add error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
