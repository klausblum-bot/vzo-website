"""Read-only: Inhalt des Juni-Backups pruefen (Rettungsquelle) + debug.log."""
import os, stat, datetime, zipfile, collections, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)


def ts(m):
    return datetime.datetime.utcfromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')


def show(p, limit=200):
    print("--- ls %s" % p)
    try:
        for e in sorted(s.listdir_attr(p), key=lambda a: a.filename)[:limit]:
            kind = 'd' if stat.S_ISDIR(e.st_mode) else '-'
            print("  %s %s %12d %s  %s" % (kind, oct(stat.S_IMODE(e.st_mode)), e.st_size, ts(e.st_mtime), e.filename))
    except Exception as ex:
        print("  FEHLER: %s" % ex)


def walk_files(base, cap=8000):
    out = []
    stack = [base]
    n = 0
    while stack and n < cap:
        cur = stack.pop()
        try:
            entries = s.listdir_attr(cur)
        except Exception:
            continue
        for e in entries:
            n += 1
            if stat.S_ISDIR(e.st_mode):
                stack.append(cur + "/" + e.filename)
            else:
                out.append((cur + "/" + e.filename, e.st_size, e.st_mtime))
    return out, n


print("========== A) uploads-old (korrekter Pfad) je Jahresordner")
for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]:
    base = "/public_html/wp-content/updraft/uploads-old/" + y
    try:
        entries = s.listdir_attr(base)
    except Exception as ex:
        print("  %s: FEHLER %s" % (y, ex)); continue
    tot = 0
    for e in sorted(entries, key=lambda a: a.filename):
        if stat.S_ISDIR(e.st_mode):
            files, _ = walk_files(base + "/" + e.filename)
            tot += len(files)
            if files:
                print("  %s/%s: %d Dateien" % (y, e.filename, len(files)))
    print("  %s GESAMT: %d Dateien" % (y, tot))

print("========== B) Juni-Backup herunterladen und Inhalt pruefen")
name = "backup_2026-06-05-1333_Venenzentrum_Zrcher_Oberland_b836a51c0492-uploads.zip"
remote = "/public_html/wp-content/updraft/" + name
local = "/tmp/" + name
s.get(remote, local)
print("  heruntergeladen: %s (%d Bytes)" % (local, os.path.getsize(local)))

zf = zipfile.ZipFile(local)
names = zf.namelist()
print("  Eintraege im ZIP: %d" % len(names))
per_year = collections.Counter()
for n in names:
    parts = n.split('/')
    if len(parts) >= 2 and parts[0] == 'uploads':
        per_year[parts[1] if len(parts) > 1 else '?'] += 1
print("  --- Eintraege je Jahresordner im Juni-Backup:")
for k in sorted(per_year):
    print("    %s: %d" % (k, per_year[k]))

print("  --- Eintraege unter uploads/2021/03 und uploads/2021/01:")
for n in sorted(names):
    if n.startswith("uploads/2021/03/") or n.startswith("uploads/2021/01/"):
        i = zf.getinfo(n)
        print("    %10d  %s" % (i.file_size, n))

print("  --- Alle Eintraege mit 'logo' oder 'berwarth' im Namen:")
for n in sorted(names):
    low = n.lower()
    if 'logo' in low or 'berwarth' in low:
        i = zf.getinfo(n)
        print("    %10d  %s" % (i.file_size, n))

print("========== C) debug.log")
try:
    a = s.stat("/public_html/wp-content/debug.log")
    print("  Groesse: %d Bytes, mtime %s" % (a.st_size, ts(a.st_mtime)))
    with s.open("/public_html/wp-content/debug.log", 'r') as f:
        data = f.read().decode('utf-8', 'replace')
    lines = data.splitlines()
    print("  Zeilen: %d" % len(lines))
    print("  --- Anfang ---")
    for l in lines[:70]:
        print("   ", l[:220])
    print("  --- Ende ---")
    for l in lines[-30:]:
        print("   ", l[:220])
except Exception as ex:
    print("  FEHLER: %s" % ex)

s.close(); t.close()
print("FERTIG")
