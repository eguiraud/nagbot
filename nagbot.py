from telegram.ext import Updater, CommandHandler
import logging

def setup_logging():
    lvl = logging.INFO # or DEBUG
    logging.basicConfig(level=lvl,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log(*args, **kwargs):
    logging.getLogger('nagbot').info(*args, **kwargs)

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

def start_bot():
    # the updater is responsible for the background handling of telegram events
    u = Updater(token='PUT_YOUR_TOKEN_HERE')
    u.dispatcher.add_handler(CommandHandler('nag', start_nagging, pass_job_queue=True))
    u.dispatcher.add_handler(CommandHandler('stop', stop_nagging, pass_job_queue=True))
    u.start_polling()

if __name__ == '__main__':
    setup_logging()
    start_bot()
