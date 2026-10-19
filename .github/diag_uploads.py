"""Read-only: Suche nach Rettungsquelle (aeltere UpdraftPlus-Backups, uploads-old, debug.log)."""
import os, stat, datetime, paramiko

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


def walk_files(base, cap=6000):
    """Rekursiv Dateien sammeln (paramiko hat kein zuverlaessiges walk)."""
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


print("========== 1) Alle Backups im updraft-Ordner")
show("/public_html/wp-content/updraft")

print("========== 2) Dateizahl je Jahresordner im AKTUELLEN uploads")
for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026"]:
    p = "/public_html/wp-content/uploads/" + y
    try:
        entries = s.listdir_attr(p)
    except Exception as ex:
        print("  %s: FEHLER %s" % (y, ex)); continue
    for e in sorted(entries, key=lambda a: a.filename):
        if stat.S_ISDIR(e.st_mode):
            files, _ = walk_files(p + "/" + e.filename)
            print("  %s/%s: %d Dateien" % (y, e.filename, len(files)))
        else:
            print("  %s/%s: Datei" % (y, e.filename))

print("========== 3) uploads-old: Dateizahl je Jahresordner + Logo-/Berwarth-Treffer")
hits = []
for y in ["2020", "2021", "2022", "2023", "2024", "2025", "2026", "backup", "et_temp", "rank-math", "wpcode", "wp-file-manager-pro"]:
    p = "/public_html/wp-content/uploads-old/" + y
    try:
        entries = s.listdir_attr(p)
    except Exception as ex:
        print("  %s: FEHLER %s" % (y, ex)); continue
    for e in sorted(entries, key=lambda a: a.filename):
        if stat.S_ISDIR(e.st_mode):
            files, _ = walk_files(p + "/" + e.filename)
            print("  %s/%s: %d Dateien" % (y, e.filename, len(files)))
            for f, sz, m in files:
                low = f.lower()
                if "logo" in low or "berwarth" in low:
                    hits.append((f, sz, m))
        else:
            print("  %s/%s: Datei" % (y, e.filename))
print("  --- Logo-/Berwarth-Treffer in uploads-old:")
for f, sz, m in hits:
    print("    %10d %s  %s" % (sz, ts(m), f))
if not hits:
    print("    (keine)")

print("========== 4) uploads/backup (falls vorhanden)")
show("/public_html/wp-content/uploads/backup")
show("/public_html/wp-content/uploads-old/backup")

print("========== 5) debug.log (aktuell, %d Bytes)" % 0)
try:
    a = s.stat("/public_html/wp-content/debug.log")
    print("  Groesse: %d Bytes, mtime %s" % (a.st_size, ts(a.st_mtime)))
    with s.open("/public_html/wp-content/debug.log", 'r') as f:
        data = f.read().decode('utf-8', 'replace')
    print("  --- Anfang ---")
    print("\n".join(data.splitlines()[:60]))
    print("  --- Ende ---")
    print("\n".join(data.splitlines()[-40:]))
except Exception as ex:
    print("  FEHLER: %s" % ex)

s.close(); t.close()
print("FERTIG")
