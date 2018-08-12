from telegram.ext import Updater, CommandHandler

def nag(bot, job):
    bot.send_message(job.context, 'WEEEEEEEEE!')

def start_nagging(bot, update, job_queue):
    chat_id = update.message.chat.id
    job_queue.run_repeating(nag, interval=5, first=0, context=chat_id, name=chat_id)

def stop_nagging(bot, update, job_queue):
    nag_jobs = job_queue.get_jobs_by_name(update.message.chat.id)
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
    start_bot()
