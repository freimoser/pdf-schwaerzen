# PDF sicher schwärzen

**Live:** https://freimoser.github.io/pdf-schwaerzen/

Text wirklich entfernen statt nur überdecken – kostenlos, ohne Anmeldung, ohne Upload.

## Funktionen
- Echtes Schwärzen mit MuPDF (WebAssembly): Text, Bilder und Vektorgrafik unter den Flächen werden aus der Datei gelöscht; der Rest bleibt durchsuchbar.
- Rechteck ziehen (Maus/Finger), Suchen und alle Vorkommen schwärzen (mit Groß-/Kleinschreibung-Schalter).
- Automatische Vorschläge: IBAN (Prüfziffer), Steuer-ID (Prüfziffer), Kreditkarte (Luhn), BIC, SV-Nummer, KV-Nummer, Geburtsdatum, E-Mail, Telefon, PLZ + Ort, Straße + Nr., eigene Namensliste.
- Kontoauszug-Modus: ganze Buchungszeile oder nur Empfänger/Verwendungszweck.
- Bereinigung: Dokumenteigenschaften, XMP, Kommentare, Formulare, Lesezeichen, eingebettete Dateien, JavaScript, alte Versionen (Datei wird neu geschrieben).
- Prüfung der fertigen Datei; Download erst, wenn alles grün ist.

## Datenschutz
Alles läuft lokal im Browser (Web Worker). Kein Upload, kein Tracking, keine Cookies.

## Entwicklung
- `python3 build.py` erzeugt alle Seiten, Sitemap und llms.txt.
- `node test/core-test.mjs` – Kerntest (Schwärzen + unabhängige Rohsuche).

## Quellen
Siehe [quellen.md](quellen.md).

## Lizenz
AGPL-3.0, weil MuPDF unter der AGPL-3.0 steht. Siehe [LICENSE](LICENSE) und [THIRD-PARTY-LICENSES](THIRD-PARTY-LICENSES).

Thomas Freimoser · [freimoser.de](https://freimoser.de/) · München / Remote
