"""Read-only Bestandsaufnahme des Uploads-Ordners (kein Schreibzugriff)."""
import os, stat, datetime, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)


def ts(m):
    return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')


def show(p, limit=80):
    print("--- ls %s" % p)
    try:
        for e in sorted(s.listdir_attr(p), key=lambda a: a.filename)[:limit]:
            kind = 'd' if stat.S_ISDIR(e.st_mode) else '-'
            print("  %s %s %12d %s  %s" % (kind, oct(stat.S_IMODE(e.st_mode)), e.st_size, ts(e.st_mtime), e.filename))
    except Exception as ex:
        print("  FEHLER: %s" % ex)


for p in ["/public_html/wp-content/uploads",
          "/public_html/wp-content/uploads/2021",
          "/public_html/wp-content/uploads/2021/03",
          "/public_html/wp-content/uploads/backup",
          "/public_html/wp-content/uploads/backup/2021",
          "/public_html/wp-content/uploads/backup/2021/03",
          "/public_html/wp-content",
          "/public_html/wp-content/updraft"]:
    show(p)

print("--- Existenz-Checks")
for p in ["/public_html/wp-content/uploads/2021/03/Logo-VZO-HB-3-min-1-1-1-1-min-min.png",
          "/public_html/wp-content/uploads/2021/03/Logo-VZO-HB-3-min-1-1-1-1-min-min.png.webp",
          "/public_html/wp-content/uploads/2021/03/venenspezialistin-dr-berwarth-min.jpg",
          "/public_html/wp-content/uploads/2021/03/venenspezialistin-dr-berwarth-min.jpg.webp",
          "/public_html/wp-content/uploads/.htaccess",
          "/public_html/wp-content/uploads/2021/.htaccess",
          "/public_html/wp-content/uploads/2021/03/.htaccess"]:
    try:
        a = s.stat(p)
        print("  JA   %10d %s  %s" % (a.st_size, ts(a.st_mtime), p))
    except Exception as ex:
        print("  NEIN %s  (%s)" % (p, ex))

print("--- Dateizahl je Jahresordner unter uploads")
try:
    for e in s.listdir_attr("/public_html/wp-content/uploads"):
        if stat.S_ISDIR(e.st_mode):
            p = "/public_html/wp-content/uploads/" + e.filename
            n = 0
            try:
                for root, dirs, files in s.walk(p):
                    n += len(files)
            except Exception:
                pass
            print("  %-14s %5d Dateien   (mtime %s)" % (e.filename, n, ts(e.st_mtime)))
except Exception as ex:
    print("  FEHLER: %s" % ex)

print("--- Letzte 15 geaenderte Dateien unter uploads/2020 .. uploads/2025")
found = []
for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]:
    base = "/public_html/wp-content/uploads/" + y
    try:
        for root, dirs, files in s.walk(base):
            for f in files:
                try:
                    a = s.stat(root + "/" + f)
                    found.append((a.st_mtime, root + "/" + f))
                except Exception:
                    pass
    except Exception:
        pass
for m, p in sorted(found, reverse=True)[:15]:
    print("  %s  %s" % (ts(m), p))

s.close(); t.close()
print("FERTIG")
