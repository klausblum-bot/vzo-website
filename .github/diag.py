#!/usr/bin/env python3
"""TEMPORAER: read-only Runde v5 - Zeitpunkt + weitere Persistenz."""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

def ls(path, limit=60):
    print(f"===== ls {path} =====", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(path), key=lambda x: x.st_mtime, reverse=True)[:limit]:
            print(f"{stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

def head(path, n=4000):
    print(f"===== head {path} =====", flush=True)
    try:
        print(sftp.open(path, 'rb').read(n).decode('utf-8', 'replace'), flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

# Wann fingen die Fatal Errors an?
head('/public_html/wp-content/debug.log', 2500)

# Klassische Persistenz-Ablagen
ls('/public_html/wp-content')
ls('/public_html')
ls('/public_html/wp-includes')

# Home-Verzeichnis: Logs?
ls('.', 40)
for p in ['logs', 'www_logs', 'error_log', 'access_log']:
    try:
        sftp.stat(p); print(f"{p}: JA", flush=True)
    except Exception:
        pass

t.close()
