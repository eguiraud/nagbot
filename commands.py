from log import log
import scrape_lercio
from telegram import ParseMode

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
