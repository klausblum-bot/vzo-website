#!/usr/bin/env python3
"""TEMPORAER: Beweise sichern + Notfall-Reparatur www.v-zo.ch.

Schritte:
  1. Beweise (Plugin-Verzeichnis, testp.php, debug.log-Anfang) als tar.gz -> base64
  2. Quarantaene: link-case + testp.php nach /forensik-20261019/ verschieben
  3. debug.log (7,1 GB Muell) loeschen
  4. Verifikation
"""
import io, os, stat, base64, tarfile, datetime
import paramiko

host = os.environ['FTP_HOST']; user = os.environ['FTP_USER']; pw = os.environ['FTP_PASSWORD']
t = paramiko.Transport((host, 22)); t.connect(username=user, password=pw)
sftp = paramiko.SFTPClient.from_transport(t)

def ts(m): return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')

PLUGIN = '/public_html/wp-content/plugins/link-case'
QUAR = '/forensik-20261019'

def ls(path, limit=40):
    print(f"--- ls {path}", flush=True)
    try:
        for a in sorted(sftp.listdir_attr(path), key=lambda x: x.st_mtime, reverse=True)[:limit]:
            print(f"    {stat.filemode(a.st_mode)} {a.st_size:>13} {ts(a.st_mtime)} {a.filename}", flush=True)
    except Exception as e:
        print("    ERR", repr(e), flush=True)

# ---------- 1. BEWEISE ----------
print("=== 1. Beweise sichern ===", flush=True)
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    def add(remote, arc):
        data = sftp.open(remote, 'rb').read()
        info = tarfile.TarInfo(arc)
        info.size = len(data)
        info.mtime = int(sftp.stat(remote).st_mtime)
        tar.addfile(info, io.BytesIO(data))
    add(PLUGIN + '/link-case.php', 'link-case/link-case.php')
    add(PLUGIN + '/uninstall.php', 'link-case/uninstall.php')
    add(PLUGIN + '/assets/public.js', 'link-case/assets/public.js')
    add(PLUGIN + '/assets/public.css', 'link-case/assets/public.css')
    add(PLUGIN + '/languages/readme.txt', 'link-case/languages/readme.txt')
    add('/public_html/testp.php', 'testp.php')
    st = sftp.stat('/public_html/wp-content/debug.log')
    f = sftp.open('/public_html/wp-content/debug.log', 'rb')
    head = f.read(20000)
    info = tarfile.TarInfo('debug.log-erste-20KB.txt'); info.size = len(head); info.mtime = int(st.st_mtime)
    tar.addfile(info, io.BytesIO(head))
    f.seek(max(0, st.st_size - 20000))
    tail = f.read()
    info = tarfile.TarInfo('debug.log-letzte-20KB.txt'); info.size = len(tail); info.mtime = int(st.st_mtime)
    tar.addfile(info, io.BytesIO(tail))
    info = tarfile.TarInfo('debug.log-groesse.txt')
    meta = f"debug.log Groesse beim Sichern: {st.st_size} Bytes ({ts(st.st_mtime)} UTC)\n".encode()
    info.size = len(meta); info.mtime = int(st.st_mtime)
    tar.addfile(info, io.BytesIO(meta))
blob = buf.getvalue()
print(f"BEWEIS-TAR.GZ Bytes={len(blob)}", flush=True)
print("BEWEIS_B64_START", flush=True)
print(base64.b64encode(blob).decode(), flush=True)
print("BEWEIS_B64_END", flush=True)

# ---------- 2. QUARANTAENE ----------
print("=== 2. Quarantaene ===", flush=True)
try:
    sftp.mkdir(QUAR); print(f"mkdir {QUAR} ok", flush=True)
except Exception as e:
    print("mkdir:", repr(e), flush=True)

try:
    sftp.rename(PLUGIN, QUAR + '/link-case')
    print(f"verschoben: {PLUGIN} -> {QUAR}/link-case", flush=True)
except Exception as e:
    print("rename Plugin ERR:", repr(e), flush=True)

try:
    sftp.rename('/public_html/testp.php', QUAR + '/testp.php')
    print(f"verschoben: /public_html/testp.php -> {QUAR}/testp.php", flush=True)
except Exception as e:
    print("rename testp ERR:", repr(e), flush=True)

# ---------- 3. LOG LEEREN ----------
print("=== 3. debug.log loeschen ===", flush=True)
try:
    st = sftp.stat('/public_html/wp-content/debug.log')
    print(f"vorher: {st.st_size} Bytes", flush=True)
    sftp.remove('/public_html/wp-content/debug.log')
    print("debug.log entfernt", flush=True)
except Exception as e:
    print("remove debug.log ERR:", repr(e), flush=True)

# ---------- 4. VERIFIKATION ----------
print("=== 4. Verifikation ===", flush=True)
ls('/public_html/wp-content/plugins')
ls(QUAR)
ls('/public_html')
for p in ['/public_html/wp-content/plugins/link-case', '/public_html/testp.php',
          '/public_html/wp-content/debug.log']:
    try:
        sftp.stat(p); print(f"{p}: existiert noch!", flush=True)
    except Exception:
        print(f"{p}: weg ✓", flush=True)

t.close()
