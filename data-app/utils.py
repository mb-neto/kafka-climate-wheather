from datetime import datetime
from pytz import timezone

class bcolors:
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def log_scope(color: str, *args, **kw):
    date = datetime.now()
    tz = timezone('America/Manaus')
    print(color + f'[{date.astimezone(tz)}]' + bcolors.ENDC, *args, **kw)

def _print(*args, **kw):
    log_scope(bcolors.OKBLUE, *args, **kw)

def _error(*args, **kw):
    log_scope(bcolors.FAIL, *args, **kw)

def _warning(*args, **kw):
    log_scope(bcolors.WARNING, *args, **kw)