#!/usr/bin/env python3
"""TEMPORAER: read-only Runde v6 - Zugriffslogs (wurde die Hintertuer benutzt?)."""
import os, stat, datetime, re
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

print("===== ls www_logs =====", flush=True)
try:
    for a in sorted(sftp.listdir_attr('www_logs'), key=lambda x: x.st_mtime, reverse=True)[:40]:
        print(f"{stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
except Exception as e:
    print("ERR", repr(e), flush=True)

print("===== ls .tmp =====", flush=True)
try:
    for a in sorted(sftp.listdir_attr('.tmp'), key=lambda x: x.st_mtime, reverse=True)[:20]:
        print(f"{stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
except Exception as e:
    print("ERR", repr(e), flush=True)

def scan(path, patterns, nbytes=600000):
    print(f"===== scan {path} (letzte {nbytes} Bytes) =====", flush=True)
    try:
        st = sftp.stat(path)
        print(f"size={st.st_size} mtime={ts(st.st_mtime)}", flush=True)
        f = sftp.open(path, 'rb'); f.seek(max(0, st.st_size - nbytes))
        lines = f.read().decode('utf-8', 'replace').splitlines()
        print(f"[{len(lines)} Zeilen gelesen]", flush=True)
        for pat in patterns:
            hits = [l for l in lines if pat in l]
            print(f"--- Treffer fuer '{pat}': {len(hits)}", flush=True)
            for l in hits[:15]:
                print("   ", l[:300], flush=True)
        # erste 500er-Zeile und Zeitraum
        e500 = [l for l in lines if ' 500 ' in l]
        if e500:
            print(f"--- 500er: {len(e500)}, erster: {e500[0][:200]}", flush=True)
            print(f"--- letzter: {e500[-1][:200]}", flush=True)
        if lines:
            print(f"--- Zeitraum: {lines[0][:80]} ... {lines[-1][:80]}", flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

for name in ['vzo-access.log', 'access.log', 'vzo-error.log', 'error.log']:
    try:
        sftp.stat('www_logs/' + name)
        scan('www_logs/' + name, ['_d5a55e', 'data-ops84', 'link-case', 'gvTOhiF2XT'])
    except Exception:
        pass

t.close()
