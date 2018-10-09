import json
import os
import time
import traceback

from . import logger
from .remote import server_req_ping


def get_token():
    class NoToken(Exception):
        pass

    def get_token_from_config():
        try:
            fn = os.path.expanduser('~/.dt-shell/config')
            if os.path.exists(fn):
                s = open(fn).read()
                j = json.loads(s)
                return j['token_dt1']
        except Exception as e:
            raise NoToken(str(e))

    if 'DT1_TOKEN' in os.environ:
        return os.environ['DT1_TOKEN']

    try:
        return get_token_from_config()
    except NoToken:
        raise


def main():
    while True:

        try:
            one()
        except Exception as e:

            logger.error(traceback.format_exc(e))

        time.sleep(2)
        break


class Storage:
    npings = 0


def get_stats():
    stats = dict()

    stats['npings'] = Storage.npings

    Storage.npings += 1

    try:
        import uptime
        stats['uptime'] = uptime.uptime()
    except:
        stats['uptime'] = None

    return stats

def one():
    token = get_token()
    stats = get_stats()
    print stats
    res = server_req_ping(token, stats)
    print res

