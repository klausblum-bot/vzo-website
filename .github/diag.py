#!/usr/bin/env python3
"""TEMPORAER: read-only Abschlusskontrolle v9."""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)
def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

print("=== debug.log jetzt ===", flush=True)
try:
    st = sftp.stat('/public_html/wp-content/debug.log')
    print(f"wieder da: {st.st_size} Bytes, mtime {ts(st.st_mtime)}", flush=True)
except Exception as e:
    print("noch nicht wieder da ✓", flush=True)

print("=== Dateien in www_logs/v-zo.ch mit Datum >= 2026-10-15 ===", flush=True)
try:
    for a in sorted(sftp.listdir_attr('www_logs/v-zo.ch'), key=lambda x: x.filename):
        if a.filename.endswith('.gz'):
            if a.filename >= 'access.log.20261015':
                print(f"    {a.st_size:>12} {ts(a.st_mtime)} {a.filename}", flush=True)
        else:
            print(f"    {a.st_size:>12} {ts(a.st_mtime)} {a.filename}   <-- KEIN .gz", flush=True)
except Exception as e:
    print("ERR", repr(e), flush=True)

def tail(path, n=1500000):
    st = sftp.stat(path)
    f = sftp.open(path, 'rb'); f.seek(max(0, st.st_size - n))
    return st, f.read().decode('utf-8', 'replace').splitlines()

for p in ['www_logs/v-zo.ch/access.log']:
    print(f"=== {p} ===", flush=True)
    try:
        st, lines = tail(p)
        print(f"size={st.st_size} mtime={ts(st.st_mtime)} Zeilen={len(lines)}", flush=True)
        print("erste:", lines[0][:150] if lines else '-', flush=True)
        print("letzte:", lines[-1][:150] if lines else '-', flush=True)
        for pat in ['link-case', '_d5a55e', 'data-ops84', 'POST /wp-login', 'POST /wp-admin', 'xmlrpc']:
            h = [l for l in lines if pat in l]
            print(f"--- '{pat}': {len(h)}", flush=True)
            for l in h[:10]:
                print("   ", l[:250], flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

t.close()
