#!/usr/bin/env python3
"""TEMPORAER: read-only Runde v7 - Zugriffslog v-zo.ch."""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

def ls(path, limit=40):
    print(f"===== ls {path} =====", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(path), key=lambda x: x.st_mtime, reverse=True)[:limit]:
            print(f"{stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

ls('www_logs/v-zo.ch')

def scan(path, patterns, nbytes=800000):
    print(f"===== scan {path} =====", flush=True)
    try:
        st = sftp.stat(path)
        print(f"size={st.st_size} mtime={ts(st.st_mtime)}", flush=True)
        f = sftp.open(path, 'rb'); f.seek(max(0, st.st_size - nbytes))
        lines = f.read().decode('utf-8', 'replace').splitlines()
        print(f"[{len(lines)} Zeilen, ab: {lines[0][:120] if lines else '-'}]", flush=True)
        print(f"[bis: {lines[-1][:120] if lines else '-'}]", flush=True)
        for pat in patterns:
            hits = [l for l in lines if pat in l]
            print(f"--- '{pat}': {len(hits)} Treffer", flush=True)
            for l in hits[:12]:
                print("   ", l[:280], flush=True)
        e500 = [l for l in lines if '" 500 ' in l or ' 500 ' in l]
        print(f"--- 500er im Ausschnitt: {len(e500)}", flush=True)
        for l in e500[:3]:
            print("   E ", l[:250], flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

for p in ['www_logs/v-zo.ch/access.log', 'www_logs/v-zo.ch/v-zo.ch-access.log',
          'www_logs/v-zo.ch/error.log', 'www_logs/v-zo.ch/v-zo.ch-error.log']:
    try:
        sftp.stat(p); scan(p, ['_d5a55e', 'data-ops84', 'link-case', 'gvTOhiF2XT'])
    except Exception:
        pass

t.close()
