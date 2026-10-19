#!/usr/bin/env python3
"""TEMPORAER: read-only Diagnose des WP-500-Fehlers auf dem v-zo.ch-Host."""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']
user = os.environ['FTP_USER']
pw = os.environ['FTP_PASSWORD']

t = paramiko.Transport((host, 22))
t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)


def ls(path, limit=60):
    print(f"===== ls {path} =====", flush=True)
    try:
        items = sorted(sftp.listdir_attr(path), key=lambda a: a.st_mtime, reverse=True)
        for a in items[:limit]:
            ts = datetime.datetime.utcfromtimestamp(a.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{stat.filemode(a.st_mode)} {a.st_size:>13} {ts} {a.filename}")
    except Exception as e:
        print("ERR", repr(e))
    print(flush=True)


def head(path, nbytes=1500):
    print(f"===== head {path} =====", flush=True)
    try:
        f = sftp.open(path, 'rb')
        print(f.read(nbytes).decode('utf-8', 'replace'))
    except Exception as e:
        print("ERR", repr(e))
    print(flush=True)


def tail(path, nbytes=150000, nlines=120):
    print(f"===== tail {path} =====", flush=True)
    try:
        st = sftp.stat(path)
        print(f"size={st.st_size} mtime={datetime.datetime.utcfromtimestamp(st.st_mtime)}")
        f = sftp.open(path, 'rb')
        f.seek(max(0, st.st_size - nbytes))
        data = f.read().decode('utf-8', 'replace')
        for ln in data.splitlines()[-nlines:]:
            print(ln[:600])
    except Exception as e:
        print("ERR", repr(e))
    print(flush=True)


def exists(path):
    try:
        sftp.stat(path)
        return True
    except Exception:
        return False


print("=== Existenz-Checks ===")
for p in ['/public_html/.maintenance', '/public_html/wp-content/.maintenance',
          '/public_html/wp-content/plugins/link-case', '/public_html/testp.php']:
    print(f"{p}: {'JA' if exists(p) else 'nein'}")
print(flush=True)

ls('/public_html/wp-content/upgrade')
ls('/public_html/wp-content/upgrade-temp-backup')
ls('/public_html/wp-content/plugins/link-case')
head('/public_html/wp-content/plugins/link-case/link-case.php')
tail('/public_html/wp-content/debug.log')

t.close()
