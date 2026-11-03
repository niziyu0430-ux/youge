"""WSGI deployment adapter for the same routes used by the local website.

Gunicorn owns network parsing, concurrency and proxy integration. The existing
handler runs against a bounded in-memory request, preserving the questionnaire,
login and static-file behavior without running a development HTTP listener.
"""
from __future__ import annotations

from io import BytesIO
import os
from types import SimpleNamespace
from urllib.parse import quote_from_bytes

from .access import AccessController, password_record
from .web import Handler, WEB_CONFIG, load_config

MAX_BODY = 2_000_000
HOP_HEADERS = {'connection', 'keep-alive', 'proxy-authenticate',
               'proxy-authorization', 'te', 'trailer', 'transfer-encoding', 'upgrade'}


class _Socket:
    def __init__(self, request):
        self.input = BytesIO(request)
        self.output = BytesIO()

    def makefile(self, mode, buffering=-1):
        return self.input

    def sendall(self, data):
        self.output.write(data)


class _Handler(Handler):
    def log_message(self, format, *args):
        # Gunicorn owns access/error logs. Never log request bodies or tokens.
        pass


def create_app(*, controller=None):
    """Require an explicit deployment secret; never provision a public default."""
    if controller is None:
        secret = os.environ.get('YOUGE_ACCESS_PASSWORD', '')
        if not secret:
            raise RuntimeError('Set YOUGE_ACCESS_PASSWORD in the hosting platform before deployment.')
        controller = AccessController(password_record(secret))
    load_config(WEB_CONFIG)
    server = SimpleNamespace(access_control=controller, server_name='youge', server_port=0)

    def application(environ, start_response):
        try:
            length = int(environ.get('CONTENT_LENGTH') or '0')
        except ValueError:
            return _error(start_response, '400 Bad Request')
        if length < 0 or length > MAX_BODY:
            return _error(start_response, '413 Content Too Large')
        body = environ['wsgi.input'].read(length) if length else b''
        if len(body) != length:
            return _error(start_response, '400 Bad Request')
        target = quote_from_bytes((environ.get('SCRIPT_NAME', '') +
                                   environ.get('PATH_INFO', '/')).encode('latin-1'),
                                  safe="/:@!$&'()*+,;=-._~")
        if environ.get('QUERY_STRING'):
            target += '?' + environ['QUERY_STRING']
        method = environ.get('REQUEST_METHOD', 'GET')
        headers = []
        for name, value in environ.items():
            if name.startswith('HTTP_'):
                header = name[5:].replace('_', '-')
                if header.lower() not in HOP_HEADERS | {'content-length'}:
                    headers.append((header, str(value)))
        if environ.get('CONTENT_TYPE'):
            headers.append(('Content-Type', environ['CONTENT_TYPE']))
        headers.extend([('Content-Length', str(length)), ('Connection', 'close')])
        if any('\r' in item or '\n' in item for pair in headers for item in pair) or any(
                c in target + method for c in '\r\n'):
            return _error(start_response, '400 Bad Request')
        request = (f'{method} {target} HTTP/1.0\r\n' +
                   ''.join(f'{name}: {value}\r\n' for name, value in headers) + '\r\n').encode('latin-1') + body
        connection = _Socket(request)
        _Handler(connection, (environ.get('REMOTE_ADDR', 'unknown'), 0), server)
        raw_headers, _, response_body = connection.output.getvalue().partition(b'\r\n\r\n')
        lines = raw_headers.decode('latin-1').split('\r\n')
        if not lines or not lines[0].startswith('HTTP/'):
            return _error(start_response, '500 Internal Server Error')
        status = lines[0].split(' ', 1)[1]
        response_headers = []
        for line in lines[1:]:
            name, value = line.split(':', 1)
            if name.lower() not in HOP_HEADERS:
                response_headers.append((name, value.strip()))
        start_response(status, response_headers)
        return [response_body]

    return application


def _error(start_response, status):
    body = b'{"error":"Invalid request"}'
    start_response(status, [('Content-Type', 'application/json'),
                            ('Content-Length', str(len(body))), ('Cache-Control', 'no-store')])
    return [body]
