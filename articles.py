# Ratgeberseiten (per exec aus build.py eingebunden)
TOOLBTN = f'<p><a class="btn pri" href="{P}">PDF jetzt kostenlos schwärzen →</a></p>'

PAGES.append(("kontoauszug-schwaerzen/", page("kontoauszug-schwaerzen/", "Kontoauszug schwärzen: Jobcenter, Wohngeld, BAföG",
 "Kontoauszug schwärzen: Was du fürs Jobcenter, Wohngeld oder BAföG schwärzen darfst und was sichtbar bleiben muss – mit Anleitung, kostenlos und ohne Upload.",
 "Kontoauszug schwärzen",
 "Beim Kontoauszug darfst du in der Regel bei Ausgaben Empfänger und Verwendungszweck schwärzen, wenn sie besonders sensible Daten verraten – Datum und Betrag müssen aber lesbar bleiben. So machst du es richtig.",
 f'''<h2>Die Grundregel</h2>
<p>Das Bundessozialgericht hat entschieden, dass Leistungsbeziehende Kontoauszüge vorlegen müssen, bei <strong>Ausgaben</strong> aber Empfänger bzw. Verwendungszweck schwärzen dürfen, wenn diese besondere Arten personenbezogener Daten offenbaren – etwa Zahlungen an Parteien, Gewerkschaften oder Religionsgemeinschaften. Der <strong>Betrag muss sichtbar bleiben</strong> (BSG, Urteil vom 19.09.2008, Az. B 14 AS 45/07 R). <strong>Einnahmen</strong> dürfen nicht geschwärzt werden, weil sie für den Anspruch zählen.</p>
<table><thead><tr><th>Teil der Buchung</th><th>Schwärzen?</th></tr></thead><tbody>
<tr><td>Datum, Betrag</td><td>Nein, muss lesbar bleiben</td></tr>
<tr><td>Einnahmen (Gehalt, Unterhalt, Überweisungen an dich)</td><td>Nein</td></tr>
<tr><td>Empfänger/Zweck bei sensiblen Ausgaben (z. B. Partei, Gewerkschaft, Kirche, Arzt, Beratungsstelle)</td><td>In der Regel ja</td></tr>
<tr><td>Ausgaben des täglichen Lebens</td><td>Im Zweifel bei der Stelle nachfragen</td></tr></tbody></table>
<h2>Jobcenter / Bürgergeld</h2><p>Hier gilt die BSG-Entscheidung direkt: Kontoauszüge (meist der letzten drei Monate) vorlegen, sensible Ausgaben-Empfänger schwärzen, Beträge stehen lassen. Wenn das Jobcenter nachfragt, wofür eine geschwärzte Ausgabe war, genügt meist eine allgemeine Angabe.</p>
<h2>Wohngeld</h2><p>Die Wohngeldstelle prüft Einkommen und Miete. Einnahmen und Mietzahlung müssen erkennbar sein. Für sensible Ausgaben gilt dieselbe Überlegung wie beim Jobcenter; frag im Zweifel bei deiner Stelle nach.</p>
<h2>BAföG</h2><p>Beim BAföG geht es vor allem um Vermögen zum Zeitpunkt der Antragstellung. Kontostand und Einnahmen bleiben sichtbar; einzelne sensible Ausgaben-Empfänger kannst du nach derselben Logik schwärzen.</p>
<h2>Finanzamt, Steuererklärung und Vermieter</h2><p>Finanzamt: Nur was du als Beleg einreichst, muss lesbar sein – andere Buchungen auf demselben Auszug darfst du schwärzen. Vermieter: Wer Zahlungsnachweise verlangt, braucht nur die Mietzahlungen; alles andere kannst du schwärzen.</p>
<h2>So geht’s mit dem Tool (Kontoauszug-Modus)</h2>
<ol><li>Kontoauszug-PDF im <a href="{P}">Tool</a> öffnen.</li><li>„Buchungen finden“ mit „nur Empfänger/Zweck“ – Datum und Betrag bleiben stehen.</li><li>Nur die sensiblen Buchungen anhaken, „Schwärzen &amp; prüfen“.</li><li>Grüne Prüfliste – herunterladen.</li></ol>
<h2>Am iPhone</h2><p>Das <a href="{P}">Tool</a> läuft auch in Safari. Kontoauszug aus der Banking-App als PDF in „Dateien“ sichern, im Tool öffnen, mit dem Finger markieren. Mehr dazu: <a href="{P}pdf-schwaerzen-mac-iphone/">PDF schwärzen am Mac und iPhone</a>. Warum Markieren mit dem Stift oft nicht reicht: <a href="{P}sicher-schwaerzen/">sicher schwärzen</a>.</p>
<p class="small">Quelle: Bundessozialgericht, Urteil vom 19.09.2008, B 14 AS 45/07 R. Stand {STAND}.</p>{TOOLBTN}''',
 [("Darf ich beim Jobcenter-Kontoauszug etwas schwärzen?", "Ja, bei Ausgaben Empfänger und Verwendungszweck, wenn sie sensible Daten verraten. Beträge und Einnahmen müssen sichtbar bleiben (BSG, B 14 AS 45/07 R)."),
  ("Muss der Kontostand sichtbar sein?", "Ja, Kontostand, Daten und Beträge braucht die Stelle zur Prüfung."),
  ("Reicht es, mit dem Textmarker schwarz drüberzumalen?", "Auf Papier oft ja, in einer PDF meist nicht: Der Text darunter bleibt häufig kopierbar. Nutze ein Werkzeug, das den Text entfernt."),
  ("Wird mein Kontoauszug hochgeladen?", "Nein, das Tool verarbeitet die PDF nur in deinem Browser.")],
 extra_ld=[howto("Kontoauszug schwärzen", ["Kontoauszug-PDF im Tool öffnen", "Buchungen finden (nur Empfänger/Zweck)", "Sensible Buchungen auswählen und Schwärzen & prüfen", "Geprüfte Datei herunterladen"])])))

PAGES.append(("sicher-schwaerzen/", page("sicher-schwaerzen/", "PDF schwärzen sicher: Warum ein Balken nicht reicht",
 "PDF schwärzen sicher: Wie schlechte Schwärzungen sichtbar gemacht werden und welche Methode Text wirklich entfernt. Vergleich, Selbsttest und Tipps für Praxen.",
 "PDF sicher schwärzen: Warum ein schwarzer Kasten nicht reicht",
 "Ein schwarzer Kasten in einer PDF ist oft nur eine Zeichnung über dem Text – der Text darunter bleibt in der Datei und lässt sich kopieren. Sicher ist nur eine Schwärzung, die den Text aus der Datei entfernt.",
 f'''<h2>So werden schlechte Schwärzungen sichtbar gemacht</h2>
<ul><li><strong>Text kopieren:</strong> Bereich unter dem Balken markieren, kopieren, in einen Editor einfügen. Liegt der Text noch darunter, erscheint er.</li>
<li><strong>Balken verschieben:</strong> Ist der Balken ein Kommentar oder eine Form, lässt er sich in vielen PDF-Programmen anklicken und verschieben oder löschen.</li>
<li><strong>Metadaten:</strong> Titel oder Autor verraten oft genau den Namen, der im Text geschwärzt wurde – siehe <a href="{P}pdf-metadaten-entfernen/">Metadaten entfernen</a>.</li>
<li><strong>Alte Versionen:</strong> PDFs können inkrementell gespeichert werden; frühere Fassungen stecken dann noch in der Datei.</li></ul>
<p>Ein öffentlich breit berichteter Fall: Im Januar 2019 ließ sich in einem Gerichtsdokument der Verteidigung von Paul Manafort der geschwärzte Text durch einfaches Kopieren lesbar machen.</p>
<h2>Die drei Methoden im Vergleich</h2>
<table><thead><tr><th>Methode</th><th>Text wirklich weg?</th><th>Rest durchsuchbar?</th><th>Dateigröße</th></tr></thead><tbody>
<tr><td>Schwarzer Kasten / Kommentar drüber</td><td>Nein</td><td>Ja</td><td>unverändert</td></tr>
<tr><td>Seite als Bild speichern</td><td>Ja (auf dieser Seite)</td><td>Nein, nur noch Bild</td><td>meist größer</td></tr>
<tr><td>Echtes Schwärzen (Redaction)</td><td>Ja</td><td>Ja</td><td>meist ähnlich</td></tr></tbody></table>
<p>Dieses <a href="{P}">Tool</a> nutzt echtes Schwärzen mit MuPDF und prüft danach automatisch, ob unter den Flächen noch Text steht und ob die Begriffe irgendwo in der Datei vorkommen.</p>
<h2>Selbsttest in 30 Sekunden</h2><ol><li>Geschwärzte PDF öffnen.</li><li>Strg+F (Mac: ⌘+F) nach dem geschwärzten Wort suchen.</li><li>Den Bereich unter dem Balken markieren und kopieren.</li></ol><p>Findet die Suche nichts und kommt beim Einfügen nichts heraus, ist der sichtbare Text weg.</p>
<h2>Befunde schwärzen in der Praxis</h2><p>Praxen geben Befunde an Versicherungen, Gutachter oder Patienten weiter. Schwärze Daten Dritter (z. B. Angehörige) und alles, was der Empfänger nicht braucht, und entferne die Metadaten – Praxissoftware schreibt dort oft Benutzernamen hinein. Röntgen- oder MRT-Bilder exportierst du anonym mit dem <a href="https://freimoser.github.io/dicom-viewer/">DICOM Viewer</a>. Zum Kontoauszug: <a href="{P}kontoauszug-schwaerzen/">Kontoauszug schwärzen</a>.</p>{TOOLBTN}''',
 [("Kann man eine PDF-Schwärzung sichtbar machen?", "Nur wenn sie schlecht gemacht ist: Liegt der Text noch unter dem Balken, lässt er sich kopieren. Bei echtem Schwärzen ist er aus der Datei gelöscht."),
  ("Ist das Umwandeln in ein Bild sicher?", "Für den sichtbaren Text ja, aber der Text ist dann auch an ungeschwärzten Stellen nicht mehr durchsuchbar, und Metadaten können bleiben."),
  ("Wie prüfe ich eine Schwärzung?", "Nach dem geschwärzten Wort suchen und den Bereich unter dem Balken kopieren. Dieses Tool macht das automatisch."),
  ("Werden auch Bilder unter dem Balken entfernt?", "Ja, die betroffenen Bildpixel werden überschrieben.")])))

PAGES.append(("pdf-metadaten-entfernen/", page("pdf-metadaten-entfernen/", "PDF Metadaten entfernen – PDF anonymisieren, kostenlos",
 "PDF Metadaten entfernen: Was in Autor, Titel, XMP & Co. stehen kann, wie du es ansiehst und kostenlos ohne Upload entfernst, um eine PDF zu anonymisieren.",
 "PDF Metadaten entfernen",
 "PDF-Metadaten entfernst du, indem die Dokumenteigenschaften, XMP-Daten und versteckte Inhalte gelöscht und die Datei komplett neu geschrieben wird. Das Tool macht das beim Schwärzen automatisch mit.",
 f'''<h2>Was in PDF-Metadaten stehen kann</h2>
<table><thead><tr><th>Bereich</th><th>Beispiel</th></tr></thead><tbody>
<tr><td>Dokumenteigenschaften</td><td>Autor (oft der Benutzername am PC), Titel, Betreff, Stichwörter</td></tr>
<tr><td>Software &amp; Datum</td><td>Erstellendes Programm, Erstellungs- und Änderungsdatum</td></tr>
<tr><td>XMP-Metadaten</td><td>Dieselben Angaben noch einmal, teils mit Bearbeitungsverlauf</td></tr>
<tr><td>Kommentare, Formularfelder</td><td>Notizen, ausgefüllte Felder</td></tr>
<tr><td>Lesezeichen, eingebettete Dateien, JavaScript</td><td>Inhaltsverzeichnis mit Namen, angehängte Originaldateien</td></tr>
<tr><td>Ältere Versionen</td><td>Bei inkrementellem Speichern bleibt der alte Stand in der Datei</td></tr></tbody></table>
<h2>Metadaten ansehen</h2><p>Windows: Rechtsklick → Eigenschaften → Details. Mac: in Vorschau „Werkzeuge → Informationen einblenden“. Im <a href="{P}">Tool</a> siehst du nach dem Öffnen eine Liste aller gefundenen Metadaten und versteckten Inhalte.</p>
<h2>Metadaten entfernen – so geht’s</h2><ol><li>PDF im <a href="{P}">Tool</a> öffnen.</li><li>„Metadaten &amp; versteckte Inhalte entfernen“ ist standardmäßig an.</li><li>Optional Stellen schwärzen, dann „Schwärzen &amp; prüfen“. Ohne Markierung wird nur bereinigt.</li><li>Die Prüfliste zeigt, ob noch etwas übrig ist.</li></ol>
<h2>PDF anonymisieren</h2><p>Metadaten sind nur ein Teil. Zum Anonymisieren gehören auch Namen, Adressen und Kennnummern im Text – dafür gibt es die automatischen Vorschläge. Mehr: <a href="{P}sicher-schwaerzen/">sicher schwärzen</a>, <a href="{P}kontoauszug-schwaerzen/">Kontoauszug schwärzen</a>.</p>{TOOLBTN}''',
 [("Was sind PDF-Metadaten?", "Zusatzangaben wie Autor, Titel, Software und Datum, die nicht auf der Seite sichtbar sind, aber in der Datei stehen."),
  ("Reicht es, die Eigenschaften im PDF-Programm zu leeren?", "Nicht immer: XMP-Daten und alte Versionen können bleiben, wenn die Datei nur inkrementell gespeichert wird."),
  ("Entfernt das Tool auch Kommentare?", "Ja, Kommentare, Formularfelder, Lesezeichen, eingebettete Dateien und JavaScript werden mit entfernt."),
  ("Bleibt der Text durchsuchbar?", "Ja, die Bereinigung ändert den sichtbaren Inhalt nicht.")])))

PAGES.append(("pdf-schwaerzen-mac-iphone/", page("pdf-schwaerzen-mac-iphone/", "PDF schwärzen Mac Vorschau & iPhone – was wirklich hält",
 "PDF schwärzen am Mac mit Vorschau und am iPhone: Welche Bordmittel Text entfernen, welche nur überdecken, und wie du das Ergebnis selbst prüfst.",
 "PDF schwärzen am Mac (Vorschau) und iPhone",
 "Am Mac hat Vorschau ein eigenes Schwärzen-Werkzeug; am iPhone gibt es mit „Markieren“ nur Zeichenwerkzeuge, die den Text darunter nicht zuverlässig entfernen. Prüfe das Ergebnis immer selbst – oder nutze das Tool im Browser.",
 f'''<h2>Mac: Vorschau</h2><p>In neueren macOS-Versionen bietet Vorschau unter <strong>Werkzeuge → Schwärzen</strong> ein Werkzeug, das laut Apple-Hilfe den markierten Text dauerhaft entfernt. Wichtig ist der Unterschied zu einem schwarzen <em>Rechteck</em> aus den Markierungswerkzeugen: Das ist nur eine Form über dem Text. Metadaten entfernt Vorschau dabei nicht automatisch.</p>
<h2>iPhone und iPad</h2><p>In „Dateien“ oder Mail kannst du PDFs mit „Markieren“ bemalen. Das sind Zeichnungen bzw. Anmerkungen – ob der Text darunter danach noch in der Datei steckt, hängt davon ab, wie gespeichert wird. Verlass dich nicht darauf. Im Browser geht es sicher: Das <a href="{P}">Tool</a> läuft auch in Safari am iPhone, Rechtecke ziehst du mit dem Finger.</p>
<table><thead><tr><th>Weg</th><th>Text entfernt?</th><th>Metadaten bereinigt?</th></tr></thead><tbody>
<tr><td>Mac Vorschau: Werkzeug „Schwärzen“</td><td>Laut Apple ja – selbst prüfen</td><td>Nein</td></tr>
<tr><td>Mac/iPhone: schwarzes Rechteck aus „Markieren“</td><td>Nicht zuverlässig</td><td>Nein</td></tr>
<tr><td>Dieses Tool im Browser</td><td>Ja, mit automatischer Prüfung</td><td>Ja (abschaltbar)</td></tr></tbody></table>
<h2>Ergebnis selbst prüfen</h2><p>Geschwärzte PDF öffnen, nach dem geschwärzten Wort suchen und den Bereich unter dem Balken kopieren. Mehr dazu: <a href="{P}sicher-schwaerzen/">sicher schwärzen</a> und <a href="{P}pdf-metadaten-entfernen/">Metadaten entfernen</a>. Kontoauszug aus der Banking-App: <a href="{P}kontoauszug-schwaerzen/">Kontoauszug schwärzen</a>.</p>{TOOLBTN}''',
 [("Kann ich am Mac ohne Zusatzsoftware schwärzen?", "Ja, Vorschau hat in neueren macOS-Versionen ein Schwärzen-Werkzeug. Prüfe das Ergebnis per Suche und Kopieren."),
  ("Reicht ein schwarzer Stift am iPhone?", "Nicht zuverlässig. Nutze ein Werkzeug, das den Text entfernt, und prüfe das Ergebnis."),
  ("Funktioniert das Tool in Safari?", "Ja, am Mac, iPhone und iPad, ohne App und ohne Upload.")])))

PAGES.append(("datenschutz/", page("datenschutz/", "Datenschutz – PDF sicher schwärzen",
 "Datenschutzerklärung von PDF sicher schwärzen: PDFs werden nur lokal im Browser verarbeitet, es werden keine Daten erhoben.",
 "Datenschutz", "Kurz: Deine PDFs verlassen nie dein Gerät. Es gibt keine Anmeldung, keine Cookies und kein Tracking.",
 f'''<h2>Verantwortlicher</h2><p>Thomas Freimoser, Kontaktdaten siehe <a href="https://freimoser.github.io/freimoser.de/impressum/">Impressum</a>.</p>
<h2>Verarbeitung deiner PDFs</h2><p>PDFs werden ausschließlich in deinem Browser mit MuPDF (WebAssembly) verarbeitet. Sie werden nicht hochgeladen, nicht gespeichert und nicht übermittelt.</p>
<h2>Hosting</h2><p>Die Seite wird über GitHub Pages (GitHub Inc., USA) ausgeliefert. Beim Aufruf verarbeitet GitHub technisch notwendige Zugriffsdaten wie die IP-Adresse (Art. 6 Abs. 1 lit. f DSGVO). Siehe <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung von GitHub</a>.</p>
<h2>Analyse</h2><p>{"Mit deiner Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) wird Google Analytics geladen. Ohne Zustimmung wird nichts geladen. Deine Entscheidung wird nur im localStorage gespeichert; widerrufen kannst du sie <a href='#' onclick='psConsentReset();return false'>hier</a>." if GA_ID else "Es findet keine Analyse und kein Tracking statt."}</p>
<h2>Deine Rechte</h2><p>Du hast die Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch und Beschwerde bei einer Aufsichtsbehörde.</p>''', [], article=False)))
