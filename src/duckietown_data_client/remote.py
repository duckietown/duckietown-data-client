import json
import os
import urllib2

from .utils import raise_wrapped, indent

from . import logger
from .constants import DataClientConstants


class Storage(object):
    done = False


def get_data_server_url():
    V = DataClientConstants.ENV_VAR
    default = DataClientConstants.DEFAULT_SERVER
    if V in os.environ:
        use = os.environ[V]
        if not Storage.done:
            msg = 'Using server %s instead of default %s' % (use, default)
            logger.info(msg)
            Storage.done = True
        return use
    else:
        return default


class RequestException(Exception):
    pass


class ConnectionError(RequestException):
    """ The server could not be reached or completed request or
        provided an invalid or not well-formatted answer. """


class RequestFailed(RequestException):
    """
        The server said the request was invalid.

        Answered  {'ok': False, 'error': msg}
    """


def make_server_request(token, endpoint, data=None, method='GET', timeout=3):
    """
        Raise RequestFailed or ConnectionError.

        Returns the result in 'result'.
    """
    server = get_data_server_url()
    url = server + endpoint

    headers = {'X-Messaging-Token': token}
    if data is not None:
        data = json.dumps(data)
    req = urllib2.Request(url, headers=headers, data=data)
    req.get_method = lambda: method
    try:
        res = urllib2.urlopen(req, timeout=timeout)
        data = res.read()
    except urllib2.HTTPError as e:
        msg = 'Operation failed for %s' % url
        msg += '\n\n' + e.read()
        raise ConnectionError(msg)

    except urllib2.URLError as e:
        msg = 'Cannot connect to server %s' % url
        raise_wrapped(ConnectionError, e, msg, compact=True)
        raise

    try:
        result = json.loads(data)
    except ValueError as e:
        msg = 'Cannot read answer from server.'
        msg += '\n\n' + indent(data, '  > ')
        raise_wrapped(ConnectionError, e, msg, compact=True)
        raise

    if not isinstance(result, dict) or 'ok' not in result:
        msg = 'Server provided invalid JSON response. Expected a dict with "ok" in it.'
        msg += '\n\n' + indent(data, '  > ')
        raise ConnectionError(msg)

    if result['ok']:
        if 'result' not in result:
            msg = 'Server provided invalid JSON response. Expected a field "result".'
            msg += '\n\n' + indent(result, '  > ')
            raise ConnectionError(msg)
        return result['result']
    else:
        msg = 'Failed request for %s:\n%s' % (url, result.get('error', result))
        raise RequestFailed(msg)


def server_req_ping(token, stats):
    endpoint = '/rest/ping'
    method = 'PUT'
    data = dict(stats=stats)
    return make_server_request(token, endpoint, data=data, method=method)
