# BRAND.md — Venenzentrum Zürcher Oberland (v-zo.ch)

_Marken-/Design-Stamm für die Neuerstellung der Website. Verpflichtend: Farben, Typo und Fakten aus dieser Datei, NICHT aus dem Gedächtnis. Alles belegt von www.v-zo.ch (Stand bei Projektstart)._

## Auftrag
Erneuerung der Website: **gleiche Farben, ähnliches Design**, aber **ohne WordPress/DIVI** — statisch generiertes HTML (self-contained, kein CMS). Modern, vertrauenswürdig, klinisch sauber, mobil-first.

## Farbpalette (belegt aus Live-CSS)
| Zweck | Farbe | Hex |
|---|---|---|
| Primär (Links, Buttons, Akzente, CTA) | DIVI-Blau | `#2ea3f2` |
| Sekundär (dunklere Akzente) | dunkleres Blau | `#337cd6` |
| Überschriften/Text | dunkles Grau | `#313131` |
| Zusatz-Text | Mittelgrau | `#666666` |
| Grundfläche | Weiss | `#ffffff` |

Ton: flach, keine Verläufe-Überkultur; klarer Blau/Weiss-Auftritt für medizinische Seriosität und Ruhe.

## Logo & Bildmaterial (echte Assets, im WordPress-Upload verfügbar)
- Logo: `wp-content/uploads/2021/03/Logo-VZO-HB-3-min-1-1-1-1-min-min.png.webp` (und Logo-VZO-HB-3-min.png.webp)
- Ärztin-Porträt: `uploads/2021/03/venenspezialistin-dr-berwarth-min.jpg.webp`, `Dr.Hilde-Berwarth-1-min.jpg.webp`, `Hilde-300.jpg.webp`
- Praxis: `uploads/2020/12/Venenzentrum-Praxis-8-1-1024x429.jpg.webp`, `Venenzentrum-Praxis-13-1024x655-1-300x192.jpg`
- Team: `uploads/2025/09/Natalie-Sabater.jpg.webp`; Carmelina-Klopfenstein (Venenzentrum-Praxis-13)
- Absolute Pfade: `https://www.v-zo.ch/wp-content/uploads/…`

## Praxis-/Kontaktdaten (verbindlich)
- Name: **Venenzentrum Zürcher Oberland** (AG)
- Leitung: **Dr. med. Hilde Berwarth** (Fachärztin Chirurgie/Unfallchirurgie, Phlebologie-Fähigkeitsausweis SGP, endovenöse Ablation USGG, Ultraschall SGUM)
- Adresse: **Zentralstrasse 21, CH-8623 Wetzikon**
- Telefon: **044 552 30 00** · E-Mail: **kontakt@v-zo.ch**
- Sprechstunden (2026): **Mo–Do 08:00–17:00 Uhr**; 12:00–14:00 Uhr telefonisch nicht erreichbar
- ÖV: ab HB Wetzikon, Bus 850/851 bis **Kempten Kreuzackerstrasse** (zvv.ch)
- 4 Parkplätze vor der Praxis; ebenerdig, **rollstuhlgerecht**
- Termin: **online buchbar** (im WordPress Link `…/termin-buchen-neu/`; ersatzweise eigene Anfrage/Sprungmarke)

## Leistungen (Behandlungsspektrum — Fakten aus /therapien/ + /venensystem/)
- **Diagnostik „Venencheck"**: farbcodierte Duplexsonographie (Ultraschall), Ersttermin ~45 min
- **Endovenöse Therapien (EVT)** — ambulant, Lokalanästhesie, schmerzarm, meist nur wenige Tage arbeitsunfähig:
  - ClosureFast (Medtronic), Laser (ELVeS Radial/Biolitec), Radiofrequenz
  - VenaSeal (Acrylat-Venenkleber; **wird von Kassen derzeit nicht bezahlt**)
- **Phlebektomie** (Häkchenmethode) — 2. Schritt, meist gleiche Sitzung
- **Schaumsklerotherapie** — v. a. Rezidivvarizen
- **Chirurgische Crossektomie/Stripping**: wird im Zentrum selbst NICHT mehr durchgeführt → stattdessen teilstationär/stationär in **Partnerkliniken**
- **Besenreiser**: nur noch in Verbindung mit Venentherapie (seit 01.02.2022 keine neuen Besenreiser-Patienten)
- Aufklärungsthemen auf /venensystem/: Lipödem, Lymphödem
- Kassenleistung: EVT-Verfahren werden seit **01.01.2016** von der Krankenkasse vergütet (mit Fähigkeitsausweis)

## Zielgruppen & Nutzen
- Patientinnen/Patienten mit Krampfadern/Venenleiden im Kanton Zürich (ZH Oberland, Wetzikon)
- Argumente: gesamtes Spektrum **aus einer Hand**, in einer Sitzung; ambulant & schmerzarm; kurze Heilung; Rezidiv-Rate korrekt behandelter Varizen ~5 %; frühe Behandlung bei Hautveränderung wichtig.

## Stil- & Ton-Vorgaben
- Professionell, sachlich, einfühlsam; „Praxis statt Klinik-Großbetrieb"; fachlich fundiert (Studien/Bundesamt-Belege erwähnen) aber für Laien verständlich.
- Medizinische Aussagen exakt aus BRAND.md/Quelle übernehmen; KEINE Gesundheitsversprechen erfinden.
- CTA: „Termin online buchen" prominent; Telefon prominent sichtbar.

## Startseiten-Layout (Original, belegt aus Roh-HTML 19.09.2026)
Aufbau von oben nach unten (gilt 1:1 für index.html; Header auf allen Seiten identisch):
1. **Header**: ganz oben schmale Kontakt-Leiste (Telefon 044 552 30 00, E-Mail; = DIVI `top-header`/`et-secondary-menu`), darunter **Logo** (`Logo-VZO-HB-3-min-1-1-1-1-min-min.png.webp`, 1264x187) und Hauptnavigation (Start, Venensystem, Therapien, Venenspezialistin, Termin).
2. **Direkt unter dem Header**: GROSSES Bannerfoto Dr. Berwarth `uploads/2021/03/venenspezialistin-dr-berwarth-min.jpg.webp` (1200x469px; srcset 980x383/480x188; fetchpriority high; volle Breite, max 1200px), breit unter dem Logo.
3. **2-Spalten-Sektion**: links (ca. 2/3) H1 „Venenzentrum Zürcher Oberland" + Intro-Absätze zu Dr. Berwarth (belegte Sätze, Links auf /venensystem/ und /therapien/); rechts (ca. 1/3) Telefon gross + `kontakt@v-zo.ch` (mailto) + „Sprechstunden in 2026:"-Tabelle.

## Technik (wie ABS-Projekt, aus `webdesign-html-deliverables`)
- Einzeldatei-HTML, `lang="de"`, valide; flache Sektionen; mobile-first; Dark/Light optional.
- Externe Referenzen minimieren (nur evtl. Google Fonts); echte Bildmaterial-URLs aus wp-content einbetten; fehlende Varianten ehrlich als CSS-Platzhalter kennzeichnen.

## Design-Stand NEU (Final, verifiziert 09.2026) — Verpflichtend, überstimmt obenstehende Farb/‑Layout-Tabelle
Stand aller 5 Seiten (`index`, `venensystem`, `therapien`, `venenspezialistin`, `termin`; je self-contained, CSS inline, `lang=de`). Aus den abgeschlossenen Kanban-Karten t_55641f5d → t_28c96c70 → t_57e46ed6 → t_86a9216f → t_f96d3836 → t_1d74919f.

**Aufbau (von oben nach unten, auf ALLEN Seiten identisch):**
1. Kontaktleiste `topbar`: bg `var(--blue-dark)` = **`#337cd6`**, weisser Text, Telefon 044 552 30 00 + E-Mail.
2. **Sticky-Hauptmenü** (`header.main`, `position:sticky;top:0;z-index:1000`, weiss) — nur `<nav>`; Kontaktleiste + Logo scrollen normal weg.
3. **Logo volle Breite** (`.brand-row .container{max-width:1200px}`, `img{width:100%;max-width:1200px;margin:0 auto}`).
4. **Bannerfoto Dr. Berwarth** (`venenspezialistin-dr-berwarth-min.jpg.webp`, 1200×469, `fetchpriority high`, volle Breite).
5. Inhalt in `.container{max-width:1200px;margin:0 auto;padding:0 20px}` — **exakt so breit wie das Logo, bündig**.
6. Footer: dunkel **`#222`** (unten `#1f1f1f`), heller Text, kein hellblauer Rahmen.

**Farben final (CSS-Variablen in jeder Seite):**
- `--blue` = **`#2ea3f2`** → nur dezente Text-Links.
- `--blue-strong` = **`#337cd6`** → Buttons, CTA (`.contact-strip`), aktiver Menüpunkt (`nav.main-nav a.active`), = **exakt das Header-Blau** (auf Wunsch angeglichen).
- `--blue-dark` = **`#337cd6`** → Kopf-Kontaktleiste (`var(--blue-dark)`).
- Footer `#222`/`#1f1f1f`; Grund `#ffffff`; Karten `#f5fafd`; Rahmenlinie `#e5eef5`; Überschrift `#313131`; Text `#666666`.
- **Keine hellblauen (ü2ea3f2) Akzentflächen** in grossen Flächen; nur Links richtig.

**Sektion „Die Praxis & Ihr Team" (index.html, `.team-block`):**
- Links: **Praxis-Foto** (`Venenzentrum-Praxis-8-1-1024x429`) gross (`.team-block .praxis-img{flex:1 1 60%;height:100%;object-fit:cover;border-radius:0}`).
- Rechts: `.cards{flex:0 1 40%;display:flex;flex-direction:column;gap}`, beide Karten untereinander; **oben Carmelina Klopfenstein, unten Natalie Sabater** (je richtiges Foto); `.team-block .card{width:100%;border-radius:0}`.
- **Alle Foto-Container/Fotos eckig** (`border-radius:0`), keine runden Ecken.
- Mobile (max-width:760px): `.team-block{flex-direction:column}`.

**Weitere feste Elemente:** Google-Maps-iframe (`maps.google.com/?q=Zentralstrasse+21,+8623+Wetzikon`, 250px, lazy); Praxis-Foto NUR im Team-Block; Banner bleibt volle Breite.

**Grundregeln:** die Farb-/Akzent-Behauptungen oben (alte Tabelle zeile `#2ea3f2` als „Buttons/CTA") sind überholt — Buttons/Kopf sind `#337cd6`. Kontaktdaten und Leistungen siehe frühere Abschnitte. Lieferung für Klaus stets als `vzo-website.zip` (entpacken + `index.html` öffnen).

## Veröffentlichungs-Fahrplan (Go-Live) — Klaus' Plan, abgesegnet
Klaus' Vorgehen ist grundsätzlich richtig: (1) Seiten hier fertigstellen → (2) Staging-Subdomain `www.neu.v-zo.ch` anlegen → (3) Repo bei GitHub, Commits zur Versionierung/Rollback → (4) sobald fertig, per DNS-Update auf `www.v-zo.ch` schalten und WordPress ablösen. Wichtig ist der **geplante Umstieg**

Checkliste (Punkte, die nicht vergessen werden dürfen — v. a. der erste):
1. **BILDER!** Aktuell zeigen die Seiten auf absolute WordPress-URLs (`https://www.v-zo.ch/wp-content/uploads/...`). Solange WP lebt, ok. Beim Ablösen von WordPress brechen ALLE Bilder → **alle Bilder mit in den neuen statischen Upload/Repo kopieren** und die Seiten auf relative/mitgelieferte Pfade umstellen. Grösster Fallstrick. **[ERLEDIGT — 09.2026]** Die 22 Bilder sind heruntergeladen nach `medien/uploads/…` (Original-Unterordnerstruktur 2020/12, 2021/03, 2023/03, 2025/09); alle 5 Seiten verweisen relativ auf `medien/…` (verifiziert: 27/27 vorhanden, 0 fehlend, keine `wp-content`-URL mehr). `vzo-website.zip` enthält `medien/` mit.
2. **Kein Doppelinhalt im Test:** während `neu.v-zo.ch` läuft → `noindex,nofollow` in die Seiten. **[ERLEDIGT — 09.2026]** Eingebaut in alle 5 Seiten (Commit `ef440ae`), über GitHub-Actions-SFTP-Deploy auf `/public_html/neu/` ausgespielt und live auf `neu.v-zo.ch` verifiziert (Meta-Zeile wird ausgeliefert). **Beim Switch sofort entfernen**, sonst wird die Live-Seite nicht indexiert.
3. **DNS + SSL als eigener Schritt:** „Umbenennen" = `www`-CNAME-Eintrag auf den neuen Hoster zeigen lassen + HTTPS-Zertifikat. Kasse lesen.
4. **SEO-Fundament beim Go-Live:** `sitemap.xml`, `robots.txt`, eindeutige `canonical`-Tags auf `www.v-zo.ch`, gute Meta-Descriptions.
5. **URL-Pfade passend zum Original lassen** (`/venensystem/`, `/therapien/`, `/venenspezialistin/`, `/termin/`) — keine Rankings/Lesezeichen brechen.
6. **Alte Links prüfen:** z. B. `/termin-buchen-neu/`-Verweise und sonstige WordPress-Unterseiten-Verlinkungen auf die neuen statischen Pfade umbiegen.
7. **E-Mail/Namen intakt:** `kontakt@v-zo.ch` (Hostinger) hängt NICHT am WordPress-Webhosting — beim Hoster/DNS-Umzug Mail-Konto nicht mit abbauen.
8. **Rollback:** sauberer Git-Branch/Tag; WordPress erst abbauen, NACH DEM alle Inhalte+Bilder auf der Ziel-Domain verifiziert sind.
