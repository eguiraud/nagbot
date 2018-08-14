## Nagbot: a telegram bot to nag your friends

### Installation

Assuming a linux environment with a working [conda installation](https://conda.io/docs/user-guide/install/index.html), a nagbot-friendly environment can be setup with
```bash
$ git clone https://github.com/bluehood/nagbot
$ cd nagbot
$ conda env create -f environment.yml
$ conda activate nagbot
```

Before starting the bot, remember to edit `nagbot.py` to insert a valid token at bot's creation.
Bot tokens are managed by [@BotFather](https://telegram.me/BotFather).

### Starting the bot

Within the `nagbot` conda environment (or any other environment that satisfies `nagbot`'s package dependencies) simply start the bot with `python nagbot.py`. It only requires a working internet connection to function correctly.

### Stopping the bot

The graceful way to stop the bot is sending a SIGINT signal to the process, e.g. with a `CTRL+C` from the command line or with `kill`, `htop`.
