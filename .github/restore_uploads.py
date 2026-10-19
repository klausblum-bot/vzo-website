"""RESTORE (von Klaus freigegeben): uploads/2021/01 + uploads/2021/03 aus dem Juni-Backup zurueckspielen."""
import os, calendar, zipfile, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)

ZIP = "/public_html/wp-content/updraft/backup_2026-06-05-1333_Venenzentrum_Zrcher_Oberland_b836a51c0492-uploads.zip"
LOCAL = "/tmp/juni-uploads.zip"
PREFIXES = ("uploads/2021/01/", "uploads/2021/03/")
REMOTE_ROOT = "/public_html/wp-content"

print("Lade Juni-Backup ...")
s.get(ZIP, LOCAL)
print("  %d Bytes" % os.path.getsize(LOCAL))
zf = zipfile.ZipFile(LOCAL)


def ensure_dir(path):
    parts = path.strip('/').split('/')
    cur = ''
    for p in parts:
        cur = cur + '/' + p
        try:
            s.stat(cur)
        except IOError:
            try:
                s.mkdir(cur)
                s.chmod(cur, 0o755)
            except Exception as ex:
                print("  mkdir-Fehler %s: %s" % (cur, ex))


todo = [n for n in zf.namelist() if n.startswith(PREFIXES) and not n.endswith('/')]
print("Dateien im Backup fuer diese zwei Ordner: %d" % len(todo))

written = skipped = failed = 0
total_bytes = 0
for n in sorted(todo):
    remote = REMOTE_ROOT + "/" + n
    info = zf.getinfo(n)
    ensure_dir(os.path.dirname(remote))
    try:
        exists = s.stat(remote).st_size > 0
    except IOError:
        exists = False
    if exists:
        skipped += 1
        continue
    tmp = "/tmp/_one"
    with zf.open(n) as src, open(tmp, 'wb') as dst:
        dst.write(src.read())
    try:
        s.put(tmp, remote)
        s.chmod(remote, 0o644)
        try:
            mt = calendar.timegm(info.date_time + (0, 0, 0))
            s.utime(remote, (mt, mt))
        except Exception:
            pass
        written += 1
        total_bytes += info.file_size
    except Exception as ex:
        failed += 1
        print("  FEHLER %s: %s" % (remote, ex))

print("========== ERGEBNIS")
print("  neu geschrieben: %d Dateien (%d Bytes)" % (written, total_bytes))
print("  uebersprungen (schon da): %d" % skipped)
print("  Fehler: %d" % failed)

print("========== KONTROLLE: die zwei Ordner auf dem Server")
for p in ["/public_html/wp-content/uploads/2021/01", "/public_html/wp-content/uploads/2021/03"]:
    try:
        e = s.listdir_attr(p)
        print("  %s: %d Eintraege" % (p, len(e)))
    except Exception as ex:
        print("  %s: FEHLER %s" % (p, ex))

print("========== KONTROLLE: die gesuchten Dateien")
for f in ["/public_html/wp-content/uploads/2021/03/Logo-VZO-HB-3-min-1-1-1-1-min-min.png",
          "/public_html/wp-content/uploads/2021/03/venenspezialistin-dr-berwarth-min.jpg",
          "/public_html/wp-content/uploads/2021/03/Logo-VZO-HB-3-min-1-1-1-1-min-min.png.webp"]:
    try:
        a = s.stat(f)
        print("  OK  %10d Bytes  %s" % (a.st_size, f))
    except Exception as ex:
        print("  FEHLT  %s  (%s)" % (f, ex))

s.close(); t.close()
print("FERTIG")
