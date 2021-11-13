import logging
import os
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram import ParseMode
from u_manager import download_utube


def error(update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Something went wrong, please try again later!"
    )


def help_command(update, context):
    update.message.reply_text("This bot was created for a me to use in my friends channel where we all post youtube song we like \n\n"
                              "so its simple paste url of youtube song and get back mp3\n"
                              "if song is more than 50mb after converting to mp3 it wont able to send it back to you because of telegram restrictions\n\n"
                              "you can use it for the same usecase:\n"
                              "create a channel => add bot to the channel => give bot admin rights => save your youtube music to channel by simple pasting url of youtube\n",
                              "for any questions/comments/requests feel free to reach out to me at @vozmarkov\n"
                              "<b>THANKS</b>", parse_mode=ParseMode.HTML)


def start_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"<b>Welcome to a simple bot for saving music from youtube vids</b>\n\n"
                             "its simple because you dont need to do any bot configs or selects after pasting a youtube url -> get back mp3 in best quality \n\n"
                             '<b>Simply</b> paste youtube url and it will send back mp3 to you \n'
                             'Add this bot to your music channel and whenever someone post a youtube vid with a song they want it will send back the mp3\n'
                             '<b>IF</b> you want the bot to clean up the url message you will have to give the bot admin rights in your channel\n\n'
                             'You can use the /help for more information .\n', parse_mode=ParseMode.HTML)


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
