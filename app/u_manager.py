# from __future__ import unicode_literals
import os
import youtube_dl
import json
from telegram.ext import CallbackContext
from db_manager import log_user

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def is_supported(url):
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and e.IE_NAME != 'generic':
            return True
    return False


def download_utube(update, context: CallbackContext):
    log_user(update.effective_chat, json.dumps(update.message.date,
                                               indent=4, sort_keys=True, default=str))
    url = update.message.text
    if is_supported(url):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            raw_filename = ydl.prepare_filename(info)
            filename = raw_filename.rsplit('.', 1)[0]+".mp3"
        message = context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Download Started: {filename}"
        )
        info = ydl.extract_info(url, download=True)
        context.bot.edit_message_text(
            chat_id=update.effective_chat.id, message_id=message.message_id, text=f"Convert Started:: {filename}")
        context.bot.send_audio(
            chat_id=update.effective_chat.id, audio=open(filename, 'rb'))
        context.bot.delete_message(
            chat_id=update.message.chat.id, message_id=message.message_id)
        context.bot.delete_message(
            chat_id=update.message.chat.id, message_id=update.message.message_id)
    try:
        os.remove(filename)
    except OSError:
        pass
