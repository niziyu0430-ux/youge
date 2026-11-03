"""Shared-password access, with opaque page-lifetime bearer tokens."""
from __future__ import annotations

import argparse
import base64
from collections import OrderedDict, deque
import getpass
import hashlib
import hmac
import json
import math
import os
from pathlib import Path
import secrets
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / '.local' / 'access.json'
PASSWORD_HINT = ROOT / '.local' / 'access-password.txt'
ITERATIONS = 600_000
SESSION_SECONDS = 12 * 60 * 60


def password_record(password: str) -> dict:
    if not isinstance(password, str) or not 4 <= len(password) <= 256:
        raise ValueError('访问密码请设置为4至256个字符。')
    salt = secrets.token_bytes(24)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATIONS)
    return {'algorithm': 'pbkdf2_sha256', 'iterations': ITERATIONS,
            'salt': base64.b64encode(salt).decode('ascii'),
            'digest': base64.b64encode(digest).decode('ascii')}


def validate_record(record: dict) -> None:
    if record.get('algorithm') != 'pbkdf2_sha256' or record.get('iterations') != ITERATIONS:
        raise ValueError('访问密码配置无效，请重新设置。')
    if len(base64.b64decode(record['salt'], validate=True)) < 16:
        raise ValueError('访问密码配置无效。')
    if len(base64.b64decode(record['digest'], validate=True)) != 32:
        raise ValueError('访问密码配置无效。')


def write_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix='.access-', dir=path.parent)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8') as stream:
            json.dump(record, stream)
            stream.write('\n')
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def provision(path: Path = DEFAULT_CONFIG) -> bool:
    if path.exists():
        validate_record(json.loads(path.read_text(encoding='utf-8')))
        return False
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    password = 'YG-' + '-'.join(''.join(secrets.choice(alphabet) for _ in range(4)) for _ in range(4))
    write_record(path, password_record(password))
    hint = path.with_name('access-password.txt')
    hint.write_text(password + '\n', encoding='utf-8')
    os.chmod(hint, 0o600)
    return True


class AccessController:
    def __init__(self, record: dict, *, config_path: Path | None = None,
                 clock=time.monotonic, session_seconds=SESSION_SECONDS,
                 failure_limit=8, failure_window=600, lock_seconds=60):
        validate_record(record)
        self.record = record
        self.config_path = config_path
        self.signature = self._signature() if config_path else None
        self.clock = clock
        self.session_seconds = session_seconds
        self.failure_limit = failure_limit
        self.failure_window = failure_window
        self.lock_seconds = lock_seconds
        self.sessions = OrderedDict()
        self.failures = OrderedDict()
        self.locked_until = {}
        self.lock = threading.RLock()
        self.hash_slots = threading.BoundedSemaphore(3)

    @classmethod
    def from_file(cls, path: Path = DEFAULT_CONFIG):
        provision(path)
        return cls(json.loads(path.read_text(encoding='utf-8')), config_path=path)

    def _signature(self):
        stat = self.config_path.stat()
        return stat.st_mtime_ns, stat.st_size

    def _refresh(self):
        if not self.config_path:
            return
        signature = self._signature()
        if signature != self.signature:
            record = json.loads(self.config_path.read_text(encoding='utf-8'))
            validate_record(record)
            self.record = record
            self.signature = signature
            self.sessions.clear()

    def _clean(self, now):
        for key, deadline in list(self.sessions.items()):
            if deadline <= now:
                self.sessions.pop(key, None)
        for client, deadline in list(self.locked_until.items()):
            if deadline <= now:
                self.locked_until.pop(client, None)
                self.failures.pop(client, None)
        while len(self.failures) > 5000:
            client, _ = self.failures.popitem(last=False)
            self.locked_until.pop(client, None)

    def login(self, password, client: str):
        if not isinstance(password, str) or not password or len(password) > 256:
            return {'error': '请输入有效的访问密码。'}, 400, None
        with self.lock:
            self._refresh()
            now = self.clock()
            self._clean(now)
            deadline = self.locked_until.get(client, 0)
            if deadline > now:
                wait = max(1, math.ceil(deadline - now))
                return {'error': f'尝试次数较多，请在{wait}秒后重试。', 'retry_after': wait}, 429, wait
            record = dict(self.record)
        if not self.hash_slots.acquire(blocking=False):
            return {'error': '当前登录较多，请稍后重试。', 'retry_after': 2}, 429, 2
        try:
            digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                       base64.b64decode(record['salt']), record['iterations'])
            matches = hmac.compare_digest(digest, base64.b64decode(record['digest']))
        finally:
            self.hash_slots.release()
        with self.lock:
            self._refresh()
            if record != self.record:
                return {'error': '访问密码已更新，请重新输入。'}, 401, None
            now = self.clock()
            # Concurrent wrong attempts cannot allow an extra attempt through an active lock.
            if self.locked_until.get(client, 0) > now:
                wait = max(1, math.ceil(self.locked_until[client] - now))
                return {'error': f'尝试次数较多，请在{wait}秒后重试。', 'retry_after': wait}, 429, wait
            if not matches:
                failures = self.failures.setdefault(client, deque())
                self.failures.move_to_end(client)
                while failures and failures[0] <= now - self.failure_window:
                    failures.popleft()
                failures.append(now)
                if len(failures) >= self.failure_limit:
                    self.locked_until[client] = now + self.lock_seconds
                    return {'error': f'尝试次数较多，请在{self.lock_seconds}秒后重试。',
                            'retry_after': self.lock_seconds}, 429, self.lock_seconds
                return {'error': '访问密码不正确，请重新输入。'}, 401, None
            self.failures.pop(client, None)
            token = secrets.token_urlsafe(32)
            self.sessions[hashlib.sha256(token.encode('ascii')).digest()] = now + self.session_seconds
            while len(self.sessions) > 10000:
                self.sessions.popitem(last=False)
            return {'access_token': token, 'expires_in': self.session_seconds}, 200, None

    def authorize(self, token: str | None) -> bool:
        if not token or len(token) > 256:
            return False
        with self.lock:
            self._refresh()
            now = self.clock()
            self._clean(now)
            key = hashlib.sha256(token.encode('utf-8')).digest()
            return self.sessions.get(key, 0) > now

    def revoke(self, token: str | None):
        if token:
            with self.lock:
                self.sessions.pop(hashlib.sha256(token.encode('utf-8')).digest(), None)


def main():
    parser = argparse.ArgumentParser(description='管理游格共用访问密码。')
    parser.add_argument('action', choices=['init', 'set-password'])
    args = parser.parse_args()
    if args.action == 'init':
        created = provision()
        print('已生成本地试用密码。' if created else '已有访问密码，保持不变。')
        print(f'本地密码文件：{PASSWORD_HINT}')
        return
    first = getpass.getpass('设置新的共用访问密码（至少4个字符）：')
    second = getpass.getpass('再次输入：')
    if not hmac.compare_digest(first.encode('utf-8'), second.encode('utf-8')):
        raise SystemExit('两次密码不同，未修改。')
    write_record(DEFAULT_CONFIG, password_record(first))
    PASSWORD_HINT.write_text(first + '\n', encoding='utf-8')
    os.chmod(PASSWORD_HINT, 0o600)
    print('密码已更新，已有登录会话将在下一次请求时失效。')


if __name__ == '__main__':
    main()
