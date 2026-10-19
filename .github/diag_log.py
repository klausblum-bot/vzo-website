"""Read-only: debug.log zeitlich auswerten."""
import os, re, collections, paramiko

HOST = os.environ["FTP_HOST"]; USER = os.environ["FTP_USER"]; PW = os.environ["FTP_PASSWORD"]
t = paramiko.Transport((HOST, 22)); t.connect(username=USER, password=PW)
s = paramiko.SFTPClient.from_transport(t)

p = "/public_html/wp-content/debug.log"
a = s.stat(p)
print("debug.log: %d Bytes" % a.st_size)
with s.open(p, 'r') as f:
    lines = f.read().decode('utf-8', 'replace').splitlines()
print("Zeilen: %d" % len(lines))

ts = collections.Counter()
for l in lines:
    m = re.match(r'\[(\d{2}-\w{3}-\d{4} \d{2}:\d{2}:\d{2}) UTC\]', l)
    if m:
        ts[m.group(1)] += 1
print("========== Zeitstempel (chronologisch), Anzahl Log-Zeilen je Sekunde:")
for k in sorted(ts, key=lambda x: (x[7:], x[3:6], x[:2])):
    print("  %s  %d" % (k, ts[k]))

print("========== Erste Zeile:")
print("  ", lines[0][:200] if lines else "(leer)")
print("========== Letzte Zeile:")
print("  ", lines[-1][:200] if lines else "(leer)")

print("========== Plugin-Ordner auf dem Server:")
for e in sorted(s.listdir_attr("/public_html/wp-content/plugins"), key=lambda x: x.filename):
    print("  %s" % e.filename)

s.close(); t.close()
print("FERTIG")
