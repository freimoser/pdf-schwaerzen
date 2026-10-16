#!/usr/bin/env python3
"""Erzeugt alle statischen Seiten von „PDF sicher schwärzen“. Aufruf: python3 build.py"""
import json, os, html
BASE = "https://freimoser.github.io/pdf-schwaerzen/"
P = "/pdf-schwaerzen/"
LASTMOD = "2026-10-17"
STAND = "17.10.2026"
GA_ID = ""  # GA4 Mess-ID, z. B. "G-XXXXXXX". Leer = kein Analytics, kein Banner.
LINKEDIN = "https://www.linkedin.com/in/freimoser"
REPO = "https://github.com/freimoser/pdf-schwaerzen"
NORECHT = "Allgemeine Information, keine Rechtsberatung."
NAV = [("", "Tool"), ("kontoauszug-schwaerzen/", "Kontoauszug"), ("sicher-schwaerzen/", "Sicher schwärzen"),
       ("pdf-metadaten-entfernen/", "Metadaten"), ("pdf-schwaerzen-mac-iphone/", "Mac & iPhone")]

def ga_snippet():
    if not GA_ID:
        return ""
    return f'''<div id="cc" class="cc" hidden><p>Darf ich mit Google Analytics anonym messen, welche Seiten genutzt werden? Deine PDFs werden dabei nie erfasst. <a href="{P}datenschutz/">Datenschutz</a></p><div class="btns"><button class="btn pri" type="button" id="ccYes">Zustimmen</button><button class="btn" type="button" id="ccNo">Ablehnen</button></div></div>
<script>(function(){{var K="ps-consent",v=localStorage.getItem(K),b=document.getElementById("cc");
function load(){{window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}window.gtag=gtag;
gtag("consent","default",{{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:"granted"}});
gtag("js",new Date());gtag("config","{GA_ID}",{{anonymize_ip:true}});var s=document.createElement("script");s.async=1;s.src="https://www.googletagmanager.com/gtag/js?id={GA_ID}";document.head.appendChild(s);}}
if(v==="yes")load();else if(v!=="no")b.hidden=false;
document.getElementById("ccYes").onclick=function(){{localStorage.setItem(K,"yes");b.hidden=true;load();}};
document.getElementById("ccNo").onclick=function(){{localStorage.setItem(K,"no");b.hidden=true;}};
window.psConsentReset=function(){{localStorage.removeItem(K);b.hidden=false;}};}})();</script>'''

CROSS = '''<aside class="xlink"><h2>Befunde und Praxis-Dateien ansehen – auch ohne Upload</h2><p>Bevor du einen Befund schwärzt, willst du ihn vielleicht erst lesen. Diese kostenlosen Viewer laufen genauso lokal im Browser:</p><div class="btns"><a class="btn pri" href="https://freimoser.github.io/dicom-viewer/">DICOM Viewer (Röntgen, CT, MRT) →</a><a class="btn pri" href="https://freimoser.github.io/ldt-bdt-viewer/">LDT &amp; BDT Viewer →</a><a class="btn pri" href="https://freimoser.github.io/gdt-viewer/">GDT Viewer →</a></div></aside>'''

ABOUT = f'''<section class="about"><div class="wrap"><img src="{P}favicon.svg" alt="" width="44" height="44"><div><h2>Über den Entwickler</h2><p><strong>Thomas Freimoser</strong> entwickelt kostenlose, datensparsame Web-Tools für Praxen, Büros und Privatleute – alles läuft im Browser, nichts wird hochgeladen. München / Remote.</p><div class="btns"><a class="btn" href="https://freimoser.de/"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg> freimoser.de</a><a class="btn" href="{LINKEDIN}" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg> LinkedIn</a><a class="btn" href="https://freimoser.de/projekte/"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><rect x="3" y="3" width="8" height="8" rx="2"/><rect x="13" y="3" width="8" height="8" rx="2"/><rect x="3" y="13" width="8" height="8" rx="2"/><rect x="13" y="13" width="8" height="8" rx="2"/></svg> Alle Projekte</a></div></div></div></section>'''

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def faq_html(faqs):
    return "<h2>Häufige Fragen</h2>" + "".join(f'<details class="faq"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faqs)
def art_ld(h1, desc, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "inLanguage": "de-DE",
            "dateModified": LASTMOD, "mainEntityOfPage": url, "author": {"@type": "Person", "name": "Thomas Freimoser", "url": "https://freimoser.de/", "sameAs": [LINKEDIN]}}
def howto(name, steps):
    return {"@context": "https://schema.org", "@type": "HowTo", "name": name, "step": [{"@type": "HowToStep", "position": i+1, "text": s} for i, s in enumerate(steps)]}

def page(path, title, desc, h1, lead, body, faqs, extra_ld=(), tool=False, article=True):
    url = BASE + path
    lds = ([faq_ld(faqs)] if faqs else []) + list(extra_ld)
    if article and path and not tool: lds.append(art_ld(h1, desc, url))
    if path: lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "PDF sicher schwärzen", "item": BASE}, {"@type": "ListItem", "position": 2, "name": h1, "item": url}]})
    nav = "".join(f'<a href="{P}{p}"{" aria-current=\"page\"" if p == path else ""}>{n}</a>' for p, n in NAV)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    note = f'<p class="small">{NORECHT} Stand: {STAND}.</p>' if article and path else ""
    tool_html = TOOL if tool else (f'<p><a class="btn pri" href="{P}">Jetzt PDF kostenlos schwärzen →</a></p>' if path != "datenschutz/" else "")
    scripts = f'<script src="{P}app.js" defer></script>' if tool else ""
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="google-site-verification" content="6pYvtFCnU7UFcQFajtMSkQ7tYMy3Z_Bt7teKiT5yKNg" />
<meta name="msvalidate.01" content="E1F30DEB311AAF5458907DB431B481AC" />
<meta property="og:type" content="website"><meta property="og:locale" content="de_DE"><meta property="og:site_name" content="PDF sicher schwärzen">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b1117">
<link rel="icon" href="{P}favicon.svg" type="image/svg+xml"><link rel="icon" href="{P}favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="{P}apple-touch-icon.png"><link rel="manifest" href="{P}site.webmanifest">
<link rel="stylesheet" href="{P}styles.css">
{ld}
<meta name="author" content="Thomas Freimoser">
</head>
<body>
<header class="top"><div class="wrap"><a class="brand" href="{P}"><img src="{P}favicon.svg" alt="" width="28" height="28">PDF sicher schwärzen</a><nav class="main">{nav}</nav></div></header>
<main class="wrap">
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{tool_html}
<div class="content">{note}{body}{CROSS if path not in ("datenschutz/", "404/") else ""}{faq_html(faqs) if faqs else ""}</div>
</main>
{ABOUT}
<footer><div class="wrap">
<p><strong>Weitere kostenlose Tools:</strong></p>
<div class="cols"><a href="https://freimoser.github.io/dicom-viewer/">DICOM Viewer</a><a href="https://freimoser.github.io/gdt-viewer/">GDT Viewer</a><a href="https://freimoser.github.io/ldt-bdt-viewer/">LDT &amp; BDT Viewer</a><a href="https://freimoser.github.io/e-rechnung-klartext/">E-Rechnung Klartext</a><a href="https://freimoser.de/">Über den Entwickler</a></div>
<p class="cols" style="margin-top:12px"><a href="https://freimoser.github.io/freimoser.de/impressum/">Impressum</a><a href="{P}datenschutz/">Datenschutz</a><a href="{REPO}">Quellcode (AGPL-3.0)</a></p>
<p>Schwärzen mit <a href="https://mupdf.com/">MuPDF</a> (AGPL-3.0, © Artifex Software) als WebAssembly – lokal im Browser. Diese Seite steht deshalb ebenfalls unter der <a href="{REPO}/blob/main/LICENSE">AGPL-3.0</a>, der komplette <a href="{REPO}">Quellcode</a> ist öffentlich. <a href="{REPO}/blob/main/THIRD-PARTY-LICENSES">Lizenzhinweise</a>. Gebaut in München / Remote.</p>
</div></footer>
{scripts}
{ga_snippet()}
</body></html>
'''

TOOL = '''
<section class="drop" id="drop" aria-label="PDF laden">
<p><strong>PDF hierher ziehen oder auswählen – auch mehrere</strong></p>
<div class="btns"><label class="btn pri">📄 PDF auswählen<input type="file" id="fileIn" accept="application/pdf,.pdf" multiple></label><button class="btn" type="button" id="sample">Beispiel-PDF ausprobieren</button></div>
<p class="small" style="margin:10px 0 0">🔒 <strong>Deine PDF bleibt auf deinem Rechner. Es wird nichts hochgeladen.</strong> Selbst prüfen: Seite laden, dann WLAN/Netz ausschalten – das Schwärzen funktioniert weiter.</p>
</section>
<div class="msg" id="msg" hidden role="status"></div>
<section id="app" hidden>
<select id="files" hidden aria-label="Datei wählen"></select>
<div class="msg" id="scan" hidden></div>
<div class="ps">
<div class="pv" id="pv" aria-label="Seitenansicht – Rechteck ziehen zum Schwärzen"></div>
<div class="panel">
<p class="small" id="cnt"></p>
<h3>1. Rechteck ziehen</h3><p class="small">Mit Maus oder Finger direkt auf der Seite. × entfernt eine Fläche.</p>
<h3>2. Suchen und schwärzen</h3>
<input type="text" id="q" placeholder="z. B. Nachname" aria-label="Suchbegriff">
<div class="row"><label><input type="checkbox" id="cs"> Groß-/Kleinschreibung</label><button class="btn" type="button" id="doSearch">Alle Vorkommen schwärzen</button></div>
<h3>3. Personendaten erkennen</h3>
<textarea id="names" rows="2" placeholder="Optional: eigene Namen, durch Komma getrennt" aria-label="Eigene Namensliste"></textarea>
<div class="row"><button class="btn" type="button" id="auto">Automatisch vorschlagen</button><button class="btn" type="button" id="allSug" hidden>Alle übernehmen</button></div>
<div class="row"><select id="ktoMode" aria-label="Kontoauszug-Modus"><option value="mid">Kontoauszug: nur Empfänger/Zweck</option><option value="line">Kontoauszug: ganze Zeile</option></select><button class="btn" type="button" id="kto">Buchungen finden</button></div>
<div class="sugs" id="sugs"></div>
<h3>4. Anwenden</h3>
<label><input type="checkbox" id="clean" checked> Metadaten &amp; versteckte Inhalte entfernen</label><br>
<label><input type="checkbox" id="label"> Hinweis „geschwärzt“ in die Fläche</label>
<p class="small" id="find"></p>
<div class="row"><button class="btn pri" type="button" id="apply">Schwärzen &amp; prüfen</button><button class="btn" type="button" id="clear">Alles zurücksetzen</button></div>
</div></div>
<section id="res" hidden class="panel"><h2>Prüfung: Text darunter wirklich weg?</h2><ul class="rep" id="rep"></ul>
<p id="bad" hidden class="msg err">Mindestens eine Prüfung ist rot. Das passiert z. B., wenn ein Begriff auch an einer Stelle steht, die du nicht markiert hast (etwa ein zweites Vorkommen oder in Metadaten bei ausgeschalteter Bereinigung). Markiere die fehlenden Stellen und wende erneut an.</p>
<p><a class="btn pri" id="dl" hidden>⬇ Geschwärzte PDF herunterladen</a></p>
<p class="small">Bitte prüfe das Ergebnis vor dem Versenden selbst. Die Originaldatei wird nicht verändert.</p></section>
</section>'''

PAGES = []
H_STEPS = ["PDF auswählen oder hineinziehen – sie bleibt auf deinem Gerät.", "Stellen markieren: Rechteck ziehen, Begriff suchen oder Vorschläge für Personendaten übernehmen.",
           "„Schwärzen & prüfen“ klicken: Text, Bilder und Grafik unter den Flächen werden aus der Datei entfernt, Metadaten bereinigt.",
           "Grüne Prüfliste ansehen und die Datei „…_geschwaerzt.pdf“ herunterladen."]
WEBAPP = {"@context": "https://schema.org", "@type": "WebApplication", "name": "PDF sicher schwärzen", "url": BASE, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Browser", "inLanguage": "de-DE",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "featureList": ["Echtes Schwärzen: Text wird entfernt, nicht überdeckt", "Automatische Erkennung von IBAN, Steuer-ID, Geburtsdatum, E-Mail, Telefon, Adresse", "Suchen und alle Vorkommen schwärzen", "Kontoauszug-Modus", "Metadaten entfernen", "Prüfung nach dem Schwärzen", "Kein Upload"],
          "author": {"@type": "Person", "name": "Thomas Freimoser", "url": "https://freimoser.de/"}}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": "PDF sicher schwärzen", "url": BASE, "inLanguage": "de-DE"}

PAGES.append(("", page("", "PDF schwärzen kostenlos – ohne Anmeldung, ohne Upload",
 "PDF schwärzen kostenlos und ohne Anmeldung: Text wird wirklich entfernt statt überdeckt, Metadaten bereinigt, Ergebnis geprüft. Läuft lokal im Browser.",
 "PDF sicher schwärzen",
 "Text wirklich entfernen statt nur überdecken – kostenlos, ohne Anmeldung, ohne Upload. Personendaten werden automatisch vorgeschlagen, Metadaten bereinigt, und eine Prüfung zeigt, dass unter den Balken nichts mehr steht.",
 f'''<h2>Was dieses Tool anders macht</h2>
<ul><li><strong>Echtes Entfernen:</strong> Text, Bilder und Vektorgrafik unter der Fläche werden aus der PDF gelöscht. Der Rest bleibt durchsuchbar und kopierbar – keine Umwandlung in Bilder.</li>
<li><strong>Automatische Vorschläge</strong> für deutsche Personendaten: IBAN (mit Prüfziffer), Steuer-ID (mit Prüfziffer), Kreditkarte (Luhn), BIC, Sozialversicherungs- und Krankenversichertennummer, Geburtsdatum, E-Mail, Telefon, PLZ + Ort, Straße + Hausnummer und Namen aus deiner Liste.</li>
<li><strong>Metadaten &amp; Verstecktes</strong> werden mit entfernt: Autor, Titel, Software, XMP, Kommentare, Formularfelder, Lesezeichen, eingebettete Dateien, JavaScript und alte Versionen.</li>
<li><strong>Sichtbare Prüfung:</strong> Die fertige Datei wird neu geöffnet und durchsucht. Erst bei Grün gibt es den Download.</li></ul>
<h2 id="befund">Befund oder Arztbrief schwärzen – Schritt für Schritt</h2>
<p>Du willst einen Befund an die Versicherung, den Arbeitgeber oder einen Anwalt schicken, aber nicht alles preisgeben? So geht es:</p>
<ol><li>Befund-PDF oben auswählen. Liegen die Daten noch als Praxis-Datei vor, kannst du sie vorher mit dem <a href="https://freimoser.github.io/ldt-bdt-viewer/">LDT &amp; BDT Viewer</a> oder dem <a href="https://freimoser.github.io/gdt-viewer/">GDT Viewer</a> ansehen.</li>
<li>„Automatisch vorschlagen“ klicken und Name, Geburtsdatum, Adresse, Versichertennummer übernehmen.</li>
<li>Diagnosen oder Absätze, die den Empfänger nichts angehen, per Rechteck markieren.</li>
<li>„Schwärzen &amp; prüfen“ – bei grüner Liste herunterladen und vor dem Versenden noch einmal ansehen.</li></ol>
<p>Warum ein schwarzer Kasten im PDF-Editor oft nicht reicht, erklärt <a href="{P}sicher-schwaerzen/">PDF sicher schwärzen</a>. Für Kontoauszüge gibt es eine eigene Anleitung: <a href="{P}kontoauszug-schwaerzen/">Kontoauszug schwärzen</a>.</p>
<h2>Grenzen</h2>
<p>Bei gescannten Seiten (nur Bild, kein Text) findet die automatische Erkennung nichts – Rechtecke funktionieren trotzdem und entfernen die Bildpixel. Sehr große PDFs brauchen etwas Zeit. Die Schwärzungs-Engine (ca. 10 MB) wird erst geladen, wenn du eine PDF auswählst.</p>''',
 [("Ist das Schwärzen wirklich kostenlos?", "Ja. Keine Anmeldung, kein Abo, kein Wasserzeichen."),
  ("Wird meine PDF hochgeladen?", "Nein. Die Verarbeitung läuft mit MuPDF als WebAssembly in deinem Browser. Du kannst nach dem Laden der Seite offline gehen und weiterarbeiten."),
  ("Kann man die Schwärzung rückgängig machen?", "Im Ergebnis nicht: Der Text unter den Flächen ist gelöscht. Deine Originaldatei bleibt aber unverändert."),
  ("Bleibt der restliche Text durchsuchbar?", "Ja. Nur die markierten Stellen werden entfernt, die Seite wird nicht in ein Bild umgewandelt."),
  ("Geht das auch am Handy?", "Ja. Rechtecke lassen sich mit dem Finger ziehen, die Schaltflächen sind groß genug für Touch.")],
 extra_ld=[WEBAPP, WEBSITE, howto("PDF schwärzen", H_STEPS)], tool=True)))

exec(open("articles.py", encoding="utf-8").read())

for path, content in PAGES:
    os.makedirs(path or ".", exist_ok=True)
    open(os.path.join(path, "index.html") if path else "index.html", "w").write(content)

open("404.html", "w").write(page("404/", "Seite nicht gefunden – PDF sicher schwärzen", "Diese Seite gibt es nicht.", "Seite nicht gefunden",
  f'Die Seite existiert nicht. Weiter zum <a href="{P}">Tool</a>, zu <a href="{P}kontoauszug-schwaerzen/">Kontoauszug schwärzen</a>, <a href="{P}sicher-schwaerzen/">sicher schwärzen</a> oder <a href="{P}pdf-metadaten-entfernen/">Metadaten entfernen</a>.', "", [], article=False)
  .replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">').replace(f'<link rel="canonical" href="{BASE}404/">', ""))

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, _ in PAGES:
    sm.append(f"  <url><loc>{BASE}{path}</loc><lastmod>{LASTMOD}</lastmod></url>")
sm.append("</urlset>")
open("sitemap.xml", "w").write("\n".join(sm) + "\n")
open("llms.txt", "w").write(f"""# PDF sicher schwärzen

> Kostenloses deutsches Web-Tool, das PDFs lokal im Browser schwärzt (MuPDF als WebAssembly, AGPL-3.0). Text, Bilder und Vektorgrafik unter den Schwärzungen werden aus der Datei entfernt, nicht nur überdeckt. Automatische Vorschläge für deutsche Personendaten (IBAN und Steuer-ID mit Prüfziffer), Kontoauszug-Modus, Metadaten-Bereinigung und eine Prüfung der fertigen Datei. Kein Upload, keine Anmeldung.

## Seiten
- [PDF schwärzen kostenlos]({BASE}): das Tool, plus Anleitung „Befund oder Arztbrief schwärzen“
- [Kontoauszug schwärzen]({BASE}kontoauszug-schwaerzen/): was man für Jobcenter, Wohngeld, BAföG schwärzen darf
- [PDF sicher schwärzen]({BASE}sicher-schwaerzen/): warum ein schwarzer Kasten nicht reicht, Methodenvergleich
- [PDF Metadaten entfernen]({BASE}pdf-metadaten-entfernen/): was in Metadaten steht und wie man es entfernt
- [PDF schwärzen am Mac und iPhone]({BASE}pdf-schwaerzen-mac-iphone/): Bordmittel ehrlich eingeordnet
- [Datenschutz]({BASE}datenschutz/)

## Verwandte Tools
- [DICOM Viewer](https://freimoser.github.io/dicom-viewer/)
- [LDT & BDT Viewer](https://freimoser.github.io/ldt-bdt-viewer/)
- [GDT Viewer](https://freimoser.github.io/gdt-viewer/)
- [Thomas Freimoser](https://freimoser.de/) · [LinkedIn]({LINKEDIN})
""")
print("ok", len(PAGES), "Seiten")
