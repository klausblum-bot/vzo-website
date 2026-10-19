#!/usr/bin/env python3
"""TEMPORAER: read-only - wo liegt das laufende Zugriffslog?"""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)
def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

for d in ['www_logs', 'logs', 'access-logs', 'history']:
    print(f"=== ls {d} ===", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(d), key=lambda x: x.st_mtime, reverse=True)[:15]:
            print(f"    {stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
    except Exception as e:
        print("    ERR", repr(e), flush=True)

print("=== Kandidaten fuer laufendes Log ===", flush=True)
for p in ['www_logs/v-zo.ch/access.log', 'www_logs/v-zo.ch/error.log',
          'www_logs/access.log', 'www_logs/v-zo.ch/access.log.20261019',
          'www_logs/v-zo.ch/v-zo.ch.access.log']:
    try:
        st = sftp.stat(p); print(f"  OK  {p}  {st.st_size} B  {ts(st.st_mtime)}", flush=True)
    except Exception as e:
        print(f"  --  {p}  ({type(e).__name__})", flush=True)

print("=== neueste .gz im v-zo.ch-Logordner (2026101*) ===", flush=True)
try:
    for a in sorted(sftp.listdir_attr('www_logs/v-zo.ch'), key=lambda x: x.filename):
        if a.filename.startswith('access.log.2026101'):
            print(f"    {a.st_size:>12} {ts(a.st_mtime)} {a.filename}", flush=True)
except Exception as e:
    print("ERR", repr(e), flush=True)

t.close()
