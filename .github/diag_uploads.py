"""Read-only: UpdraftPlus-Protokolle + Uploads-Bestand (kein Schreibzugriff)."""
import os, stat, datetime, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)


def ts(m):
    return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')


def show(p, limit=100):
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
          "/public_html/wp-content/updraft/uploads-old",
          "/public_html/wp-content/updraft/uploads-old/2021",
          "/public_html/wp-content/updraft/uploads-old/2021/03",
          "/public_html/wp-content/updraft/plugins-old"]:
    show(p)

print("--- UpdraftPlus-Protokolle (Kopf und Ende)")
for name in ["log.c90c5d85be6d.txt", "log.b5fec7e454ae.txt", "log.b5fec7e454ae-browser.txt"]:
    p = "/public_html/wp-content/updraft/" + name
    print("========== %s" % name)
    try:
        with s.open(p, 'r') as f:
            data = f.read().decode('utf-8', 'replace').splitlines()
        print("  Zeilen: %d" % len(data))
        print("  --- erste 45 ---")
        for l in data[:45]:
            print("   ", l[:200])
        print("  --- letzte 45 ---")
        for l in data[-45:]:
            print("   ", l[:200])
    except Exception as ex:
        print("  FEHLER: %s" % ex)

print("--- Existenz-Checks (Logo/Arztfoto, alle Kandidatenpfade)")
cands = []
for base in ["/public_html/wp-content/uploads/2021/03",
             "/public_html/wp-content/updraft/uploads-old/2021/03",
             "/public_html/wp-content/uploads/backup/2021/03"]:
    for f in ["Logo-VZO-HB-3-min-1-1-1-1-min-min.png",
              "Logo-VZO-HB-3-min-1-1-1-1-min-min.png.webp",
              "venenspezialistin-dr-berwarth-min.jpg",
              "venenspezialistin-dr-berwarth-min.jpg.webp"]:
        cands.append(base + "/" + f)
for p in cands:
    try:
        a = s.stat(p)
        print("  JA   %10d %s  %s" % (a.st_size, ts(a.st_mtime), p))
    except Exception:
        print("  NEIN %s" % p)

print("--- Verzeichnis-Zeitstempel von wp-content (Geschwister von updraft)")
show("/public_html/wp-content")

s.close(); t.close()
print("FERTIG")
