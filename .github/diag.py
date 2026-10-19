#!/usr/bin/env python3
"""TEMPORAER: read-only Forensik-Sichtung des v-zo.ch-Hosts (kein Schreiben)."""
import os, stat, time, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

def show(path, nbytes=8000):
    print(f"===== {path} =====", flush=True)
    try:
        f = sftp.open(path, 'rb'); d = f.read(nbytes)
        print(d.decode('utf-8', 'replace'))
        print(f"[{len(d)} bytes gelesen]")
    except Exception as e:
        print("ERR", repr(e))
    print(flush=True)

def ls(path, limit=80):
    print(f"===== ls {path} =====", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(path), key=lambda x: x.st_mtime, reverse=True)[:limit]:
            print(f"{stat.filemode(a.st_mode)} {a.st_size:>12} {ts(a.st_mtime)} {a.filename}")
    except Exception as e:
        print("ERR", repr(e))
    print(flush=True)

def walk(root, cutoff, skip=(), max_dirs=4000):
    """Rekursiv per listdir_attr (1 Roundtrip pro Verzeichnis)."""
    found, stack, ndirs, nfiles = [], [root], 0, 0
    while stack and ndirs < max_dirs:
        d = stack.pop(); ndirs += 1
        try: entries = sftp.listdir_attr(d)
        except Exception: continue
        for a in entries:
            p = d + '/' + a.filename
            if stat.S_ISDIR(a.st_mode):
                if a.filename in skip: continue
                stack.append(p)
            else:
                nfiles += 1
                if a.st_mtime >= cutoff:
                    found.append((a.st_mtime, a.st_size, p))
    print(f"[{root}: {ndirs} Ordner, {nfiles} Dateien geprueft]", flush=True)
    return found

# --- 1. Der Backdoor-Plugin-Code komplett ---
show('/public_html/wp-content/plugins/link-case/link-case.php')
show('/public_html/wp-content/plugins/link-case/uninstall.php')
ls('/public_html/wp-content/plugins/link-case/assets')
ls('/public_html/wp-content/plugins/link-case/languages')

# --- 2. Weitere Verdachtsdateien im Webroot ---
show('/public_html/testp.php')
ls('/public_html/zeit')
ls('/public_html/history')

# --- 3. Zuletzt geaenderte PHP-Dateien im ganzen Webroot ---
cutoff = time.mktime(time.strptime('2026-10-01', '%Y-%m-%d'))
skip = {'.git', '.tmp', 'cache', 'et-cache', 'updraft', 'upgrade', 'upgrade-temp-backup', 'node_modules'}
hits = []
for root in ['/public_html', '/public_html/wp-content/uploads', '/public_html/wp-content/mu-plugins',
             '/public_html/wp-content/plugins', '/public_html/wp-content/themes']:
    hits += walk(root, cutoff, skip=skip)
hits.sort(reverse=True)
print("===== Dateien geaendert seit 2026-10-01 =====", flush=True)
for m, s, p in hits:
    if p.endswith(('.php', '.phtml', '.php5', '.php7', '.shtml', '.htaccess', '.js')) or 'link' in p.lower():
        print(f"{ts(m)} {s:>10} {p}")

# --- 4. .htaccess (auf eingeschleuste Redirects pruefen) ---
show('/public_html/.htaccess', 7000)

t.close()
