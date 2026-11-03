"""Isolated loopback UI fixture. Does not read or change the user's password."""
import argparse
from http.server import ThreadingHTTPServer
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from youge.web import Handler
from youge.access import AccessController,password_record

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8766)
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.access_control=AccessController(password_record('ui-test-only-question-review'))
    try:server.serve_forever()
    finally:server.server_close()
