from telegram import ParseMode
from telegram.ext import Updater, CommandHandler
import logging
import scrape_lercio
import signal
import sys

def setup_logging():
    lvl = logging.INFO # or DEBUG
    logging.basicConfig(level=lvl,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log(*args, **kwargs):
    logging.getLogger('nagbot').info(*args, **kwargs)

def stop_bot_at_sigint(updater):
    def stop_bot(sig, frame):
        log(f'SIGINT received, stopping bot (might take a while)')
        updater.stop()
    signal.signal(signal.SIGINT, stop_bot)

def nag(bot, job):
    bot.send_message(job.context, 'WEEEEEEEEE!')

def start_nagging(bot, update, job_queue):
    chat_id = update.message.chat.id
    log(f'start nagging chat {chat_id}')
    job_queue.run_repeating(nag, interval=15, first=0, context=chat_id, name=chat_id)

def stop_nagging(bot, update, job_queue):
    chat_id = update.message.chat.id
    log(f'stop nagging chat {chat_id}')
    nag_jobs = job_queue.get_jobs_by_name(chat_id)
    # the only job with this name, if present, is the one to remove
    if nag_jobs:
        nag_jobs[0].schedule_removal()

def send_lercio_link(bot, update):
    chat_id = update.message.chat.id
    log(f'sending lercio article to chat {chat_id}')
    article = scrape_lercio.get_main_article()
    link = article['href']
    title = article['title']
    bot.send_message(chat_id, f'[{title}]({link})', parse_mode=ParseMode.MARKDOWN)

def start_bot():
    # the updater is responsible for the background handling of telegram events
    u = Updater(token='PUT_YOUR_TOKEN_HERE')

    u.dispatcher.add_handler(CommandHandler('nag', start_nagging, pass_job_queue=True))
    u.dispatcher.add_handler(CommandHandler('stop', stop_nagging, pass_job_queue=True))
    u.dispatcher.add_handler(CommandHandler('lercio', send_lercio_link))

    stop_bot_at_sigint(u)
    u.start_polling()

if __name__ == '__main__':
    setup_logging()
    start_bot()
