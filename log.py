import logging

def setup_logging():
    lvl = logging.INFO # or DEBUG
    logging.basicConfig(level=lvl,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log(*args, **kwargs):
    logging.getLogger('nagbot').info(*args, **kwargs)

