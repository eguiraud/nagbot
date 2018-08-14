import log
import commands as cmd
from telegram.ext import Updater, CommandHandler
import signal

def get_commands():
    return [
        CommandHandler('nag', cmd.start_nagging, pass_job_queue=True),
        CommandHandler('stop', cmd.stop_nagging, pass_job_queue=True),
        CommandHandler('lercio', cmd.send_lercio_link),
        CommandHandler('latest', cmd.send_lercio_latest),
    ]

def stop_bot_at_sigint(updater):
    def stop_bot(sig, frame):
        log.log(f'SIGINT received, stopping bot (might take a while)')
        updater.stop()
    signal.signal(signal.SIGINT, stop_bot)

def start_bot():
    # the updater is responsible for the background handling of telegram events
    u = Updater(token='PUT_YOUR_TOKEN_HERE')

    for c in get_commands():
        u.dispatcher.add_handler(c)

    stop_bot_at_sigint(u)
    u.start_polling()

if __name__ == '__main__':
    log.setup_logging()
    start_bot()
