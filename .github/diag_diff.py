"""Read-only Abschlusspruefung: Juni-Backup vs. Server-Bestand + debug.log."""
import os, stat, zipfile, collections, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)

ZIP = "/public_html/wp-content/updraft/backup_2026-06-05-1333_Venenzentrum_Zrcher_Oberland_b836a51c0492-uploads.zip"
LOCAL = "/tmp/juni-uploads.zip"
ROOT = "/public_html/wp-content/uploads"

print("Lade Juni-Backup ...")
s.get(ZIP, LOCAL)
zf = zipfile.ZipFile(LOCAL)

server = set()
stack = [ROOT]
while stack:
    cur = stack.pop()
    try:
        entries = s.listdir_attr(cur)
    except Exception:
        continue
    for e in entries:
        p = cur + "/" + e.filename
        if stat.S_ISDIR(e.st_mode):
            stack.append(p)
        else:
            server.add(p)
print("Dateien auf dem Server unter uploads: %d" % len(server))

backup = [n for n in zf.namelist() if not n.endswith('/')]
print("Dateien im Juni-Backup unter uploads: %d" % len(backup))

missing = [n for n in backup if (ROOT + "/" + n) not in server]
print("========== FEHLT GEGENUEBER JUNI: %d Dateien" % len(missing))
per_dir = collections.Counter('/'.join(n.split('/')[:3]) for n in missing)
for k in sorted(per_dir):
    print("  %-28s %d" % (k, per_dir[k]))

print("========== Fehlende Dateien im Detail (max 120):")
for n in sorted(missing)[:120]:
    print("  %10d  %s" % (zf.getinfo(n).file_size, n))

print("========== Wurzelverzeichnis uploads: Server vs. Backup")
sroot = sorted(p[len(ROOT) + 1:] for p in server if '/' not in p[len(ROOT) + 1:])
broot = sorted(n for n in backup if '/' not in n)
print("  Server: %s" % (sroot[:40],))
print("  Backup: %s" % (broot[:40],))
print("  'logo.png' im Backup: %s" % ("logo.png" in broot))

print("========== debug.log (Ende)")
try:
    a = s.stat("/public_html/wp-content/debug.log")
    print("  Groesse: %d Bytes" % a.st_size)
    with s.open("/public_html/wp-content/debug.log", 'r') as f:
        lines = f.read().decode('utf-8', 'replace').splitlines()
    print("  Zeilen: %d" % len(lines))
    for l in lines[-40:]:
        print("   ", l[:200])
except Exception as ex:
    print("  FEHLER: %s" % ex)

s.close(); t.close()
print("FERTIG")
