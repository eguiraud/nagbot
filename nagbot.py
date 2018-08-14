import log
import generators as gtors

from random import random
from datetime import datetime, timedelta
import itertools as it
import signal
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

def get_chat_id(update):
    return update.message.chat.id

def add_text_sender_cmd(updater, name, text_generator):
    def callback(bot, update):
        chat_id = get_chat_id(update)
        log.log(f'sending {name} to {chat_id}')
        bot.send_message(chat_id, text_generator(), parse_mode=ParseMode.MARKDOWN)
    updater.dispatcher.add_handler(CommandHandler(name, callback))

def add_image_sender_cmd(updater, name, img_url_generator):
    def callback(bot, update):
        chat_id = get_chat_id(update)
        log.log(f'sending {name} to {chat_id}')
        bot.send_photo(chat_id, img_url_generator())
    updater.dispatcher.add_handler(CommandHandler(name, callback))

def nag_job(bot, job):
    should_send_text = random() < 1.
    if should_send_text:
        bot.send_message(job.context, gtors.random_link(), parse_mode=ParseMode.MARKDOWN)
    else:
        bot.send_photo(job.context, gtors.random_image())

def start_nagging(bot, update, job_queue):
    chat_id = get_chat_id(update)
    log.log(f'start nagging chat {chat_id}')
    time = (datetime.now() + timedelta(seconds=10)).time()
    job_queue.run_daily(nag_job, time, context=chat_id, name=chat_id)

def stop_nagging(bot, update, job_queue):
    chat_id = get_chat_id(update)
    log.log(f'stop nagging chat {chat_id}')
    nag_jobs = job_queue.get_jobs_by_name(chat_id)
    # the job with this name, if present, is the one to remove
    if nag_jobs:
        nag_jobs[0].schedule_removal()

def print_help(bot, update):
    chat_id = get_chat_id(update)
    log.log(f'printing help in chat {chat_id}')
    msg = '/nag - start annoying this chat once a day\n'
    msg += '/stop - stop annoying this chat\n'
    for name, gtor in it.chain(gtors.links.items(), gtors.images.items()):
        msg += f'/{name} - {gtor.__doc__.strip()}\n'
    bot.send_message(chat_id, msg)

def stop_bot_at_sigint(updater):
    def stop_bot(sig, frame):
        log.log(f'SIGINT received, stopping bot (might take a while)')
        updater.stop()
    signal.signal(signal.SIGINT, stop_bot)

def start_bot():
    # create updater: the updater is responsible for the background handling of telegram events
    u = Updater(token='PUT_YOUR_TOKEN_HERE')

    # register bot commands
    u.dispatcher.add_handler(CommandHandler('nag', start_nagging, pass_job_queue=True))
    u.dispatcher.add_handler(CommandHandler('stop', stop_nagging, pass_job_queue=True))
    u.dispatcher.add_handler(CommandHandler('help', print_help))
    for name, gtor in gtors.links.items():
        add_text_sender_cmd(u, name, gtor)
    for name, gtor in gtors.images.items():
        add_image_sender_cmd(u, name, gtor)

    # start polling, stop on SIGINT
    stop_bot_at_sigint(u)
    u.start_polling()

if __name__ == '__main__':
    log.setup_logging()
    start_bot()
