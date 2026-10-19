#!/usr/bin/env python3
"""TEMPORAER: read-only Runde v8 - heutiges Zugriffslog v-zo.ch."""
import os, stat, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

print("===== alle Dateien in www_logs/v-zo.ch (ohne Limit) =====", flush=True)
try:
    for a in sorted(sftp.listdir_attr('www_logs/v-zo.ch'), key=lambda x: x.filename):
        print(f"{a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
except Exception as e:
    print("ERR", repr(e), flush=True)

for p in ['www_logs/v-zo.ch/access.log', 'www_logs/v-zo.ch/error.log']:
    print(f"===== stat {p} =====", flush=True)
    try:
        st = sftp.stat(p)
        print(f"size={st.st_size} mtime={ts(st.st_mtime)}", flush=True)
        n = min(st.st_size, 2000000)
        f = sftp.open(p, 'rb'); f.seek(st.st_size - n)
        lines = f.read().decode('utf-8', 'replace').splitlines()
        print(f"[{len(lines)} Zeilen]", flush=True)
        if lines:
            print("erste:", lines[0][:160], flush=True)
            print("letzte:", lines[-1][:160], flush=True)
        for pat in ['_d5a55e', 'data-ops84', 'link-case', 'gvTOhiF2XT', 'wp-login.php', 'xmlrpc.php']:
            h = [l for l in lines if pat in l]
            print(f"--- '{pat}': {len(h)}", flush=True)
            for l in h[:8]:
                print("   ", l[:240], flush=True)
        e5 = [l for l in lines if ' 500 ' in l]
        print(f"--- 500er: {len(e5)}", flush=True)
        for l in e5[:3]:
            print("   E", l[:240], flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

t.close()
