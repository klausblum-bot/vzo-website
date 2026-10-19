#!/usr/bin/env python3
"""TEMPORAER: read-only Forensik-Sichtung v4 (schnell, kein Tiefen-Scan)."""
import os, stat, time, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

def show(path, nbytes=8000):
    print(f"===== {path} =====", flush=True)
    try:
        d = sftp.open(path, 'rb').read(nbytes)
        print(d.decode('utf-8', 'replace'), flush=True)
        print(f"[{len(d)} bytes]", flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

def ls(path, limit=100):
    print(f"===== ls {path} =====", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(path), key=lambda x: x.st_mtime, reverse=True)[:limit]:
            print(f"{stat.filemode(a.st_mode)} {a.st_size:>12} {ts(a.st_mtime)} {a.filename}", flush=True)
    except Exception as e:
        print("ERR", repr(e), flush=True)

def walk(root, cutoff, max_dirs=600, maxdepth=4, exts=('.php', '.phtml', '.php5', '.php7', '.shtml')):
    found, stack, ndirs = [], [(root, 0)], 0
    while stack and ndirs < max_dirs:
        d, depth = stack.pop(); ndirs += 1
        try: entries = sftp.listdir_attr(d)
        except Exception: continue
        for a in entries:
            p = d + '/' + a.filename
            if stat.S_ISDIR(a.st_mode):
                if depth < maxdepth and a.filename not in ('.git', 'cache', 'et-cache'):
                    stack.append((p, depth + 1))
            elif a.st_mtime >= cutoff or p.endswith(exts):
                if p.endswith(exts) and (a.st_mtime >= cutoff or True):
                    found.append((a.st_mtime, a.st_size, p))
    print(f"[{root}: {ndirs} Ordner geprueft]", flush=True)
    return found

# 1. Backdoor-Plugin komplett
show('/public_html/wp-content/plugins/link-case/link-case.php')
show('/public_html/wp-content/plugins/link-case/uninstall.php')
ls('/public_html/wp-content/plugins/link-case/assets')
ls('/public_html/wp-content/plugins/link-case/languages')

# 2. Plugin-Bestand + mu-plugins
ls('/public_html/wp-content/plugins')
ls('/public_html/wp-content/mu-plugins')

# 3. Verdachtsdateien
show('/public_html/testp.php')
show('/public_html/.htaccess', 7000)
ls('/public_html/zeit')
ls('/public_html/history')

# 4. PHP-Dateien in uploads (klassisches Versteck) + kuerzlich geaenderte in plugins
cutoff = time.mktime(time.strptime('2026-10-01', '%Y-%m-%d'))
print("===== PHP-Dateien in uploads =====", flush=True)
for m, s, p in sorted(walk('/public_html/wp-content/uploads', cutoff), reverse=True):
    print(f"{ts(m)} {s:>10} {p}", flush=True)
print("===== Dateien in plugins/ geaendert seit 2026-10-01 =====", flush=True)
for m, s, p in sorted(walk('/public_html/wp-content/plugins', cutoff, max_dirs=400, maxdepth=3), reverse=True):
    if m >= cutoff:
        print(f"{ts(m)} {s:>10} {p}", flush=True)

t.close()
