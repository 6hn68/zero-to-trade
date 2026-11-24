# zero-to-trade

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md) · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · **Deutsch** · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**Sieben Etappen, von „Welches Land nehme ich überhaupt?“ bis „Das Geld ist da.“ Dazu fünfzehn Python-Skripte, die die lästigen Teile erledigen, und eine Website mit vier Tools, die direkt in Ihrem Browser laufen. Erfahrung wird nicht vorausgesetzt. Genau darum geht es.**

> Sie haben 200 Kaltakquise-E-Mails verschickt und null Antworten bekommen. Das liegt nicht an Ihrem Englisch. Das liegt an der Reihenfolge.
>
> Dieses Repo macht aus „mit dem Export anfangen“ etwas, das Sie wirklich abarbeiten können: welche Website Sie heute Nachmittag öffnen, was Sie dort eintippen und welches Ergebnis bedeutet, dass Sie bestanden haben.

> Die eine Regel unter allem hier: **Die KI macht die Schwerarbeit, Sie treffen die Entscheidungen.**

Kein Kurs zum Kaufen. Keine Bezahlstufe. Keine E-Mail-Schranke. MIT-lizenziert, V20.

> PRs sind willkommen, besonders von Leuten, die in einen Markt verkaufen, von dem dieses Repo noch nie gehört hat. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Demo in 7 Schritten: eine echte Liste einstufen und die erste Ansprache in 2 Minuten schreiben

Sie müssen vorher keine Doku lesen. Sieben Schritte, je eine Zeile, je ein Befehl zum Kopieren – insgesamt etwa 2 Minuten. Alle sieben Befehle unten wurden in diesem Repo tatsächlich ausgeführt (2026-11-22, Python 3.x, nur Standardbibliothek). Die Beispieldaten sind fiktiv; Firmennamen tragen das Präfix 【示例】 („Beispiel“).

| Schritt | In einer Zeile | Befehl (zum Kopieren) |
|---|---|---|
| 1 Liste besorgen | Kopieren Sie das Beispiel in eine eigene Datei; Ihre echten Leads kommen nur in diese Kopie | `cp examples/leads_example.csv my_leads.csv` |
| 2 Einstufen | 10 Leads in T0–T3 sortiert; 2 davon rufen Sie heute an | `python scripts/lead_score.py my_leads.csv` |
| 3 T0 prüfen | Prüfen Sie, ob ein T0 keine Briefkastenfirma ist, bevor Sie schreiben; alles, was Sie nicht angegeben haben, kommt als „zu prüfen“ zurück | `python scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 Erstkontakt schreiben | Entwurf für die Stufe T0, Englisch zum Versenden, Chinesisch für Ihre eigene Prüfung | `python scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 Nachfassen planen | Rhythmus D0/D2/D5: 3 Kontakte in 6 Tagen, nach dem dritten Schweigen ist Schluss | `python scripts/followup_plan.py --tier T0 --start 2026-11-22 --csv my_leads.csv` |
| 6 Anbieten, wenn eine Antwort kommt | Kosten + Fracht + Marge → FOB/CIF-Spanne + eine dreistufige Zugeständnisleiter | `python scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 Nachhaken, wenn es still wird | 7 Tage nach dem Angebot ohne Antwort nach dem Stand fragen – bestimmt, nicht verzweifelt | `python scripts/nudge.py --day D7 --scenario quoted` |

Nach Schritt 4 halten Sie eine Erstkontakt-E-Mail in der Hand, die Sie wirklich verschicken können; nach Schritt 5 wissen Sie, was Sie an jedem der nächsten 6 Tage tun.

Kein Python? Öffnen Sie die Website [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/) (oder doppelklicken Sie in einer lokalen Kopie auf [`index.html`](index.html)). Dort laufen vier Tools im Browser – Lead-Bewertung, Erstansprache, Nachfassplan und Angebot – mit denselben Regeln wie die Skripte, und die Oberfläche gibt es in 12 Sprachen (Menü oben rechts). Beispielliste laden → bewerten und Ihre T0 finden → Erstkontakt erzeugen und kopieren → die Platzhalter `[ ]` durch Ihren Namen, Ihre Firma und Ihr WhatsApp ersetzen → das Nachfassen nach D0/D2/D5 planen → anbieten, sobald eine Antwort kommt. Nichts wird hochgeladen: Ihre Liste verlässt nie den Browser. Der Erstkontakt-Text auf der Website ist Englisch mit chinesischer Referenz; für Texte auf Spanisch, Portugiesisch oder Arabisch nutzen Sie `outreach_gen.py --lang es/pt/ar`.

---

## Was das wirklich löst

Googeln Sie „Wie fange ich mit dem Export an?“. Sie bekommen die Erfolgsgeschichte eines Einzelnen, zweihundert SEO-Artikel, die Gratis-Vorschau eines Bezahlkurses und ein YouTube-Thumbnail, das schnelles Geld verspricht. Sie lesen alles, fühlen sich informiert – und am nächsten Morgen starren Sie auf eine Zolldaten-Website und haben keine Ahnung, was ins erste Feld gehört.

Das ist kein Mangel an Information. Es ist Information in der falschen Form: in Fragmente zerhackt, aus der Sicht der Gewinner geschrieben und genau dort zu Ende, wo Sie etwas tun müssten.

So handhaben es die meisten Tutorials. *„Sie sollten Ihre Kunden gründlich recherchieren.“* Dann: *„Recherche ist wichtig.“* Dann nichts. Sie wissen immer noch nicht, welche Felder, welche Websites, wie ein Warnsignal aussieht oder wann Sie genug geprüft haben.

Dieses Repo macht das Gegenteil: **eine Aufgabe nehmen und so lange zerlegen, bis daraus eine Handlung wird.**

| Was ein Tutorial sagt | Was dieses Repo sagt |
|---|---|
| „Recherchieren Sie den Kunden“ | L1-Screening, drei Checks: Gibt es die Website, wie lange ist die Firma eingetragen, sind die Social-Media-Konten aktiv. Fällt einer durch, ist der Lead tot. |
| „Qualität ist wichtiger als Quantität“ | 10 Leads werden in T0/T1/T2/T3 sortiert, jede Stufe mit eigenem nächsten Schritt und eigenem Zeitbudget. |
| „Fassen Sie nach“ | Tag 1, 3, 5, 7. Jedes Mal ein anderer Ansatz, und Tag 7 endet mit einer Entscheidung: dranbleiben oder fallen lassen. |
| „KI verändert den Handel“ | Fünfzehn Python-Skripte, nur Standardbibliothek (vierzehn Business-Skripte, eines davon eine Angebots-Engine, plus ein Datenschutz-Wächter). `python scripts/lead_score.py examples/leads_example.csv`, und Sie haben die vollständige Einstufung in etwa dreißig Sekunden. |

Dieselbe Information. Eine andere **Körnung**. Das ist der ganze Unterschied. Jede Aussage hier muss eine Frage überstehen: Was öffne ich heute Nachmittag, und was tippe ich ein?

Also nein, das hier ist keine Motivation. Es ist eine Checkliste und fünfzehn Skriptdateien (vierzehn Business-Skripte + ein Datenschutz-Wächter).

---

## Die sieben Etappen

Eine Kette von Anfang bis Ende: mit der Wahl eines Landes beginnen, mit Geld auf dem Konto enden. Ein Dokument pro Etappe, und jedes endet mit etwas, das Sie wirklich verwenden können.

| Etappe | Was Sie tun | Ergebnis |
|---|---|---|
| **01 Markt wählen** | Nach Sprache, Nachfrage und Hürden bewerten | 1 erster Markt + 3 Gründe, die ihn verteidigen |
| **02 Leads finden** | Vier Wege: Zolldaten, Social Media, Suche, Messen | ≥20 geprüfte Leads pro Tag |
| **03 Käufer prüfen** | L1-Screening → L2-Standard → L3-Tiefenprüfung | A/B/C-Bewertung; Betrüger aussortiert |
| **04 Kontakt aufnehmen** | Leads in T0-T3 einstufen; beim Erstkontakt drei Kanäle bespielen | Eingestufte Liste + Nachfassplan D0/D2/D5 (3 Kontakte in 6 Tagen) |
| **05 Spezifikationen klären** | Erst kleine Bitten. Der Preis kommt immer zuletzt | Spezifikation / Menge / Bestimmungshafen |
| **06 Anbieten & verhandeln** | Angebotsdisziplin: Jedes Zugeständnis kauft eine Gegenleistung | Angebot + Zugeständnisleiter + Gesprächsleitfäden |
| **07 Auftrag abwickeln** | Vertrag, Produktion, Inspektion, Dokumente, Zahlung, Fracht | Geschlossener Lieferkreislauf + Plan für Folgeaufträge |

Die Etappen-Dokumente liegen in `docs/`, eine Datei pro Etappe, alle nach derselben sechsteiligen Struktur (siehe [CONTRIBUTING.md](CONTRIBUTING.md)): **wofür diese Etappe da ist → wie Sie vorgehen, Schritt für Schritt → die Kriterien für bestanden/nicht bestanden → die klassischen Fehler → Vorlagen zum Kopieren → die KI-Prompts für diese Etappe.**

**Noch nie gemacht?** [`docs/00-getting-started.md`](docs/00-getting-started.md) setzt weder git noch Python voraus und bringt Sie in etwa 10 Minuten in Gang. Lieber schnell? [`docs/fast-path.md`](docs/fast-path.md) führt Sie in sieben Tagen von null zur ersten Antwort.

---

## Schnellstart in 30 Sekunden

**Sie wollen Python nicht installieren?** Öffnen Sie die Website: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Vier Browser-Tools – Lead-Bewertung, Erstansprache, Nachfassplan und Angebot – in 12 Oberflächensprachen. CSV einfügen, die T0-T3-Einstufung erhalten, dann den Erstkontakt, die Nachfasstermine und das Angebot. Nichts zu installieren, und nichts verlässt Ihren Browser.

Fünfzehn Skriptdateien: vierzehn Business-Skripte, eines davon die Angebots-Engine, plus ein Datenschutz-Skript (`check_private_data.py`, sucht vor dem Commit nach echten Kundendaten). Nur Standardbibliothek. Python 3.10+.

```bash
# 1. Leads einstufen. CSV rein, T0-T3 raus, jede Stufe mit ihrem nächsten Schritt.
python scripts/lead_score.py examples/leads_example.csv

# 2. Ansprache-Texte für eine Stufe entwerfen, Englisch und 中文 nebeneinander.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Den Nachfassplan erstellen. Drei Kontakte, echte Termine.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Angebot: Kosten + Fracht + Marge -> FOB/CIF-Spanne + eine dreistufige Zugeständnisleiter.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

Das gibt der erste Befehl bei 10 Beispiel-Leads tatsächlich aus. Das Skript antwortet auf Chinesisch; 【示例】 ist nur eine Markierung für „Beispiel“, und die letzte Spalte ist hier übersetzt:

| Stufe | Firma | Land | Punkte | Nächster Schritt |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Saudi-Arabien | 95 | Erstkontakt heute senden, nicht warten |
| T0 | 【示例】三角洲轮胎 | Saudi-Arabien | 88 | Erstkontakt heute senden, nicht warten |
| T1 | 【示例】阿曼蓝海 | Oman | 77 | diese Woche; Text heute entwerfen |
| T1 | 【示例】半岛汽车 | Saudi-Arabien | 71 | diese Woche; Text heute entwerfen |
| T1 | 【示例】尼罗河商贸 | Ägypten | 67 | diese Woche; Text heute entwerfen |
| T1 | 【示例】迪拜轮毂行 | VAE | 65 | diese Woche; Text heute entwerfen |
| T1 | 【示例】利雅得汽配 | Saudi-Arabien | 60 | diese Woche; Text heute entwerfen |
| T2 | 【示例】尼日利亚先锋 | Nigeria | 46 | kalter Pool, einmal täglich durchsehen |
| T3 | 【示例】黎凡特供配 | Libanon | 20 | zu wenig Infos, zuerst Kontakt + Bedarf finden |
| T3 | 【示例】利雅得零件店 | Saudi-Arabien | 10 | zu wenig Infos, zuerst Kontakt + Bedarf finden |

Zusammenfassung: **T0:2 / T1:5 / T2:1 / T3:2**. Heute kontaktieren: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. Diese Woche: 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. Vorerst liegen lassen: 【示例】黎凡特供配, 【示例】利雅得零件店.

CSV-Kopfzeile:

```
company,country,product,source,email,phone,years,contact,note
```

Nur `company` ist Pflicht. Alles andere darf leer bleiben, und leere Felder bekommen die Mindestpunktzahl. Am stärksten wirkt `source`: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

Alle fünfzehn Skripte verstehen `--help`. `lead_score.py` hat außerdem `--format json` sowie die Filter `--country` / `--product`, falls Sie die Ausgabe in eine Tabelle leiten möchten.

Die Skripte entscheiden nur, was eine Maschine entscheiden kann: Gibt es eine E-Mail-Adresse, gibt es eine Website, reicht es für die T0-Latte. Ob ein Lead Ihren Nachmittag verdient, steht in der Doku – und in Ihrem Kopf.

---

## Aufbau des Repos

```
zero-to-trade/
├── README.md              # Vollständige chinesische Fassung
├── README_EN.md           # Englische Fassung (Referenz für jede Übersetzung)
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # Spanisch, Portugiesisch, Französisch, Arabisch (RTL), Russisch, Deutsch (diese Datei), Japanisch, Koreanisch, Türkisch, Indonesisch
├── index.html             # Die Website: 4 Browser-Tools, 12 Oberflächensprachen, keine Abhängigkeiten (GitHub Pages)
├── MANIFESTO.md           # Anonym, kein Bezahlkurs: die Haltung der Marke
├── GITHUB_LAUNCH.md       # Checkliste für Launch + Promotion (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # Wie Sie beitragen + Konventionen für Doku und Code
├── CHANGELOG.md           # Änderungsprotokoll: was sich jeweils geändert hat
├── ROADMAP.md             # Roadmap: wohin die nächsten Versionen gehen
├── LICENSE                # MIT
├── docs/                  # Eine Datei pro Etappe
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 7 Tage von null zur ersten Antwort
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # Ein realistisches Rechenbeispiel für den ersten Abschluss
├── scripts/               # Lauffähiges Python, nur Standardbibliothek
│   ├── lead_score.py      # Leads in T0-T3 einstufen
│   ├── outreach_gen.py    # Ansprache-Texte je Stufe (EN/ZH + ES/PT/AR mit englischer Referenz, V13)
│   ├── followup_plan.py   # Nachfassplan D0/D2/D5 (3 Kontakte in 6 Tagen)
│   ├── quote_engine.py    # Angebots-Engine: FOB/CIF-Spanne + dreistufige Zugeständnisleiter
│   ├── due_diligence.py   # V11 Agent für Hintergrundprüfung: L1/L2/L3 + A/B/C-Bewertung + Warnsignale
│   ├── tire_pack.py       # V12 Reifenpaket: Größe + Markt → GCC-Punkte + Verzollungsdokumente + Markthinweise
│   ├── landed_cost.py     # Einstandskosten, V14: FOB + Fracht + Versicherung → CIF, plus Zoll + Zielgebühren → DDP
│   ├── trade_show.py      # Messe, V15: auf der Messe gesammelte Aussteller → 24-Stunden-Nachfassplan (Dank in 2 h, Angebotsansatz in 12 h, Anruf/WhatsApp in 24 h)
│   ├── nudge.py           # Nachhak-Bibliothek, V16: D3/D7/D14/D30 × quoted/sampled/negotiating → kurze WhatsApp-Version + längere E-Mail-Version (Englisch + Chinesisch)
│   ├── anchor_price.py    # Preisanker am Wettbewerb, V18: Konkurrenzpreisspanne aus Zolldaten + eigene Kosten → aggressive/mittlere/konservative CIF-Stufe + 5-Punkte-Checkliste
│   ├── fast_path.py     # V19 interaktiver 7-Tage-Schnellstart: --day N zeigt Aufgaben, --done N hakt ab, --progress zählt zusammen (abgestimmt mit docs/fast-path.md)
│   ├── market_rules.py    # Marktregeln: Zielmärkte, Hürden für Türkei/Brasilien, Ausschluss von Mexiko/USA/EU
│   ├── daily_video_list.py  # Tägliche Liste mit 5 Videos (3 am Vormittag, 2 am Nachmittag) mit Checks zu Größe, Markt, Verkaufsargument und Einstellungen
│   ├── fulfillment_checklist.py  # Auftragsabwicklung: PI → Anzahlung → Produktion → Prüfung → Restzahlung → Buchung → Zoll → B/L → Dokumente → Nachverkauf, harte Geld-Gates bei Anzahlung/Freigabe/Versand
│   └── check_private_data.py  # Datenschutz-Wächter: sucht vor dem Commit nach echten Kundendaten
├── examples/
│   ├── leads_example.csv  # Beispieldaten, sofort lauffähig
│   ├── leads_example_lighting.csv  # Beispiel ohne Reifen: 8 Leads für LED-Beleuchtung
│   └── trade_show_example.csv  # Beispiel-Aussteller, einer pro Interessensstufe
├── tests/                 # 586 Tests mit der Standardbibliothek
├── prompts/
│   └── AI_PROMPTS.md      # 40 Prompts zum Kopieren (28 Kern + 12 fortgeschritten), nach Etappe gruppiert
└── assets/                # Screenshots, Diagramme
```

---

## Warum Skripte und nicht nur ein Methodendokument

Die meisten Repos zum Thema „KI fürs Business“ machen dasselbe: Methodik nehmen, in einen Prompt kleben, ausliefern. Dieses hier läuft andersherum. **Erst die Disziplin, dann die Werkzeuge.**

Der Grund: **Gut im Prompten ist nicht dasselbe wie gut im Handel.** Meine Wette ist, dass Ihnen nicht die Formulierungen fehlen. Ihnen fehlt eine Methode, um zu entscheiden. Also:

- **Die Regeln sind hier das Produkt.** T0 bekommt heute eine E-Mail. T3 liegt drei Monate in der Schublade. Ein Zugeständnis, das nichts zurückbringt, ist ein Geschenk, keine Verhandlung. Kein Modell trifft diese Entscheidungen für Sie.
- **Masse geht an die KI.** 8 Leads in einem Durchgang screenen, drei Stufen Hintergrundrecherche zu 50 Firmen entwerfen, sieben Tage Nachfassvarianten erzeugen. Stunden an Arbeit, fast kein Urteilsvermögen darin.
- **Alles Wiederholbare wird zum Skript.** Wenn Einstufung ein Bauchgefühl ist, ist sie kein Standard. Also ist sie ein Skript unter 200 Zeilen ohne Abhängigkeiten, und zwei Leute, die es ausführen, kommen zum selben Ergebnis.

Wo die Grenze liegt: **Lässt es sich als `if/else` schreiben? Ins Skript. Braucht es eine Abwägung? In die Doku. Muss es klingen, als hätte es ein Mensch geschrieben? In `prompts/`.**

Kein pandas, kein OpenAI SDK, mit Absicht. Bei der Einrichtung der Umgebung geben Einsteiger auf. Wer neu im Export ist, verliert mehr Stunden mit `pip install` als mit der Kundensuche – und das ist ein dummer Ort, um Leute zu verlieren.

---

## Roadmap

> Vollständige Roadmap: [ROADMAP.md](ROADMAP.md); Änderungsverlauf: [CHANGELOG.md](CHANGELOG.md).

| Version | Status | Inhalt |
|---|---|---|
| **V13** | ✅ Ausgeliefert (2026-11-07) | Mehrsprachige Ansprache (`scripts/outreach_gen.py --lang es/pt/ar`: Texte auf Spanisch/Portugiesisch/Arabisch + englisches Original nach jedem Entwurf; die Vorlagen spiegeln die englischen T0/T1/T2 eins zu eins, ein einziges Inline-Dict im Skript) + neuer Abschnitt in `docs/04-outreach.md` (Nutzung + 3 echte Ausgaben wörtlich eingefügt) + `tests/` 80 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 7 Skriptdateien |
| **V18** | ✅ Ausgeliefert (2026-11-07) | Preisanker am Wettbewerb (`scripts/anchor_price.py`: Konkurrenzpreisspanne aus Zolldaten + eigene Kosten → aggressive/mittlere/konservative CIF-Stufe, jeweils mit Gewinnspielraum, Marge, FOB-Äquivalent, implizitem Aufschlag und wann man sie nutzt; eine 5-Punkte-Checkliste – Kosten, Fracht, Wechselkurs, Zahlungsbedingungen, Gültigkeit – vor dem Angebot, jeder offene Punkt wird markiert; Warnung unter Kosten „unter Kosten, Auftrag nicht annehmen, erst Menge gegen Preis verhandeln“; fehlender Median wird als (niedrig + hoch) / 2 geschätzt und als Schätzung markiert; `--format json` / `--audience client`) + `docs/anchor-price.md` (Nutzung + Anker-Leitfaden + 2 echte Ausgaben wörtlich eingefügt) + eine Zeile in `docs/06-quote.md` (vor dem Angebot ankern) + `tests/` 187 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 11 Skriptdateien |
| **V20** | ✅ Aktuell (2026-11-14) | Zusammenführung lokaler Änderungen + 10 Härtungsrunden: einheitliche CLI-Einstiege (Fehler in Klartext, abgestimmte Exit-Codes) + stärkere Tests (Einzelnachricht-Modus, Alias `--start-date`, Laufprotokolle) + Zahlen in der Doku abgeglichen + Beispiel ohne Reifen (8 Leads für LED-Beleuchtung) + Demoseite mit V19 synchronisiert + freundliche Fehler bei fehlerhaften CSVs (fehlende Spalte / leere Datei / nicht geschlossenes Anführungszeichen ergeben keinen Traceback mehr) + Prompts abgeglichen (der Nachfassbefehl in P04-4 bekommt `--avoid-weekend`, das Fenster in P10-2 einheitlich 48 Stunden) + Lauf-Tracing eingeführt (`logs/trace-YYYY-MM-DD.jsonl`, eine Zeile pro Lauf der drei Kernskripte) + Code aufgeräumt (gemeinsame Hilfsfunktionen an einer Stelle, netto −151 Zeilen; zwei tote Hilfsfunktionen entfernt) + `tests/` 586 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 15 Skriptdateien |
| **V19** | ✅ Ausgeliefert (2026-11-07) | Interaktiver 7-Tage-Schnellstart (`scripts/fast_path.py`: `--day N` zeigt die Aufgaben des Tages – Aufgabenname + was entstehen soll + welches Skript/Dokument; `--done N` hakt einen Tag mit Zeitstempel ab und schreibt in die `--state`-JSON-Datei, ein erneutes Abhaken meldet „bereits abgehakt“ und wird nicht doppelt erfasst; `--progress` zählt erledigt / offen / überfällig (überfällig = geplantes Datum vor heute und nicht abgehakt, geplantes Datum = `--start` Tag 1 + (N-1) Tage; ohne `--start` keine Überfällig-Zählung, das wird klar gesagt); `--list` zeigt alle 7 Tage; Aufgaben Zeile für Zeile mit `docs/fast-path.md` abgestimmt, keine zweite Liste erfunden; `--help` enthält echte Beispiele, ein ungültiger Tag oder ein ungültiges Datum ergibt einen Fehler in Klartext) + `docs/fast-path-interactive.md` (Nutzung + Format der Statusdatei + Überfällig-Regel + 7-Tage-Überblick + 2 echte Ausgaben wörtlich eingefügt) + eine Zeile oben in `docs/fast-path.md` (interaktiver Einstieg) + eine Zeile in `docs/00-getting-started.md` Schritt B5 (8 verbleibende Skripte → 9) + `tests/` 226 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 12 Skriptdateien |
| **V17** | ✅ Ausgeliefert (2026-11-07) | Vollständige READMEs auf Portugiesisch und Arabisch (neu `README_PT.md` in brasilianischem Portugiesisch und `README_AR.md` auf Arabisch mit RTL-Layout, beide vollständig übersetzt und mit README_EN.md abgeglichen: gleiche Abschnitte, Tabellen, Befehle, Skriptnamen, Dateinamen, Version und Zahlen; alle Beispielfirmen/-preise/-kontakte sind fiktiv, mit 【示例】 und der reservierten Domain sample.example markiert) + `tests/` 167 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 10 Skriptdateien |
| **V16** | ✅ Ausgeliefert (2026-11-07) | Nachhak-Bibliothek (`scripts/nudge.py`: D3/D7/D14/D30 × quoted/sampled/negotiating, insgesamt 12 Entwürfe, kurze WhatsApp-Version + längere E-Mail-Version, zuerst Englisch, nach jedem Entwurf die chinesische Übersetzung; Tonleiter – D3 sanfte Erinnerung, D7 nach dem Stand fragen, D14 drei gesichtswahrende Optionen (niedrigerer Preis / andere Spezifikation / längeres Zahlungsziel), D30 letzte Nachricht, die die Tür offen lässt; Tag 0 ist der Tag, an dem Angebot/Muster/Preisgespräch rausging – ein anderer Anker als der Erstkontakt-Rhythmus von followup_plan, ein Thread folgt nur einer Linie; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (Nutzung + Zusammenspiel mit followup_plan + 2 echte Ausgaben wörtlich eingefügt) + eine Zeile in `docs/00-getting-started.md` (Skriptliste 6 → 7) + `tests/` 152 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 10 Skriptdateien |
| **V15** | ✅ Ausgeliefert (2026-11-07) | Nachfassen nach der Messe (`scripts/trade_show.py`: auf der Messe gesammelte Aussteller nach Interesse sortiert in einen 24-Stunden-Nachfassplan – Dank + Unterlagen in 2 h, Angebotsansatz in 12 h, Anruf/WhatsApp in 24 h; `--add` einzeln + `--csv` im Stapel, `--format json` / `--out`; der Erstkontakt-Entwurf folgt der T0/T1/T2-Vorlage von outreach_gen) + `docs/trade-show.md` (Nutzung + 1 echte Ausgabe wörtlich eingefügt) + `examples/trade_show_example.csv` (3 Beispiel-Aussteller, einer pro Interessensstufe) + je eine Zeile in `docs/00-getting-started.md` und `docs/02-find-leads.md` (was nach der Messe mit den Leads zu tun ist) + `tests/` 127 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 9 Skriptdateien |
| **V14** | ✅ Ausgeliefert (2026-11-07) | Schätzung der Einstandskosten (`scripts/landed_cost.py`: FOB + Fracht + Versicherung → CIF, plus Zoll + Gebühren im Zielhafen → DDP; Kosten pro Stück + Summen + Gewinnspielraum, wenn ein Verkaufspreis angegeben ist; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (Nutzung + Formeltabelle + 2 echte Ausgaben wörtlich eingefügt) + je eine Zeile in `docs/00-getting-started.md` und `docs/06-quote.md` (FOB/CIF zuerst mit quote_engine anbieten, dann mit landed_cost die vollen Einstandskosten berechnen) + `tests/` 97 Tests mit der Standardbibliothek + 40 Prompts unverändert (28 Kern + 12 fortgeschritten) + 8 Skriptdateien |
| **V12** | ✅ Ausgeliefert (2026-11-07) | Reifenpaket (`scripts/tire_pack.py`: Größe + Markt → GCC-Zertifizierungspunkte + Verzollungsdokumente im Zielhafen + Markthinweise; 4 TBR-Größen × 8 Märkte) + `docs/tire-pack.md` (Nutzung + 2 echte Ausgaben wörtlich eingefügt) + Skriptliste in `docs/00-getting-started.md` aktualisiert + `tests/` 68 Tests mit der Standardbibliothek + 40 Prompts (28 Kern + 12 fortgeschritten) + 7 Skriptdateien |
| **V11** | ✅ Ausgeliefert (2026-11-07) | Agent für Hintergrundprüfung (`scripts/due_diligence.py`: L1/L2/L3 + A/B/C-Bewertung + Checkliste für Warnsignale + Kundenansicht + JSON-Ausgabe) + `docs/03-due-diligence.md` Abschnitt 13 (echte Ausgabe wörtlich eingefügt) + Prompt P03-5 + `tests/` 52 Tests mit der Standardbibliothek + 40 Prompts (28 Kern + 12 fortgeschritten) + 6 Skriptdateien |
| **V10** | ✅ Ausgeliefert (2026-11-07) | 6 fortgeschrittene Module (08 eigene Website / 09 Social-Media-Matrix / 10 Messen / 11 Logistik & Zahlung / 12 Risiko & Compliance / 13 Schlüsselkunden) + 3 Lernpfade + Fehlerbehebung & Ablauf für Beitragende + Angebots-Engine gehärtet (Isolierung der Kundenansicht, Grenzwertprüfungen) + `tests/` 30 Tests mit der Standardbibliothek + 39 Prompts (27 Kern + 12 fortgeschritten) + Bewertung der Browser-Demo an Python angeglichen |
| **v0.1.5** | Veröffentlicht | Browser-Demo ohne Installation (index.html) + v0.2 Angebots-Engine Alpha (quote_engine.py) + Marken-Manifest (MANIFESTO) + Checkliste für Launch/Promotion (GITHUB_LAUNCH) + Fast Path + Beispiel-Abschluss Schritt für Schritt |
| **v0.1** | Veröffentlicht | 7 Etappen-Dokumente, 4 Business-Skripte mit der Standardbibliothek, 27 Prompts, zweisprachige README |
| **v0.2** | ✅ Ausgeliefert (Alpha) | **KI-Angebots-Engine**: `scripts/quote_engine.py` ist live – Kosten + Markt + Wettbewerbs-Ankerpreis eingeben → FOB/CIF-Spanne + eine dreistufige Zugeständnisleiter (jede Stufe muss etwas einbringen); Isolierung der Kundenansicht und Grenzwertprüfungen gehärtet (siehe `tests/test_quote_engine.py`) |
| **Nächste Version** | Noch offen | Nächste Richtung noch offen (interaktiver 7-Tage-Schnellstart in V19 ausgeliefert) |
| **Langfristig** | — | Branchenpakete (Reifen, Baustoffe, Maschinen, Eisenwaren); Ansprache-Texte auf Französisch/Russisch (Spanisch, Portugiesisch und Arabisch in V13 ausgeliefert); öffentliche anonymisierte Lead-Datensätze; Anbindung der Angebots-Engine an Zolldaten für automatische Wettbewerbs-Ankerpreise |

V20 wartet nicht auf die nächste Version: Die 10 Härtungsrunden sind jetzt schon nutzbar (fehlerhafte CSVs ergeben Fehler in Klartext statt Tracebacks, jeder Lauf schreibt eine Trace-Zeile, gemeinsame Hilfsfunktionen liegen an einer Stelle). Sie müssen nicht auf die nächste Version warten – die Skripte sind bereits im Repo, und alle 586 Tests sind grün.

---

## Mitmachen

Die Lücke hier ist nicht die Doku. Es sind **länderspezifische Details aus der Praxis.** Ich weiß, wie der erste Reifenauftrag in den Nahen Osten läuft. Ich habe keine Ahnung, wie der Baustoffvertrieb in Ecuador funktioniert oder welche Dokumente der nigerianische Zoll wirklich sehen will. Das können nur Leute ergänzen, die dort verkaufen.

Drei Einstiege, der günstigste zuerst:

1. **Etwas korrigieren.** Tippfehler, veralteter Fakt, eine Regel, die sich wie Brei liest. Eröffnen Sie ein Issue. Ein Satz ist besser als Schweigen. Die Vorlage fragt drei Dinge: An welcher Zeile haben Sie den Faden verloren, welche Zahl hat keine Quelle, welche Regel gilt in Ihrer Branche nicht.
2. **Eine Etappe übersetzen.** Spanisch, Arabisch, Portugiesisch, Russisch, Französisch, Vietnamesisch – was immer Sie wirklich sprechen. Behalten Sie die sechsteilige Struktur, tauschen Sie die Sprache und gleichen Sie die Begriffe mit [GLOSSARY.md](GLOSSARY.md) ab.
3. **Ihr Land oder Ihre Branche ergänzen.** Das ist der fehlende Teil. Schreiben Sie, was Sie getan haben, nicht was man Ihrer Meinung nach tun sollte. Feldnamen, Dokumentnamen, wie der Vertriebskanal aufgebaut ist, wie bezahlt wird – und warum man sich weigert zu zahlen.

Code ebenfalls, mit einer harten Regel: **Python 3.10+, nur Standardbibliothek.** Die Begründung steht in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Für Entwickler: anpassbar und ohne Abhängigkeiten

Alle vierzehn Business-Skripte (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`, plus der Datenschutz-Wächter `check_private_data.py`) nutzen nur die Standardbibliothek. Es gibt kein `pip install`. Forken, ändern, in Ihre eigenen Projekte einbauen:

- Die Gewichtung passt Ihnen nicht? Vier Konstanten oben in `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Das Maximum bleibt 100.
- Sie haben eigene Zolldaten? Passen Sie die Kopfzeile an (`company,country,product,source,email,phone,years,contact,note`) und speisen Sie sie ein.
- Sie wollen es in Ihr eigenes Tool einbauen? Jedes Skript lässt sich sauber importieren. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` sind reine Funktionen, die Dicts und Listen zurückgeben. Kein Netzwerk, keine geschriebenen Dateien.
- Die CI führt bei jedem PR `py_compile` plus die Testsuite (Python 3.10–3.13) plus eine Datenschutzprüfung aus, damit sich keine fehlerhafte Änderung durchschleicht.

> Die Grundhaltung hier: **überprüfbar statt clever.** Verlassen Sie sich nicht auf mein Wort: Führen Sie `python scripts/lead_score.py examples/leads_example.csv` aus und lesen Sie, was herauskommt.

---

## Wenn Ihnen das einen Umweg erspart hat

Geben Sie einen Stern. Oben rechts. Mehr verlange ich nicht. So finden Sie das Repo auch in sechs Monaten wieder, wenn Sie den Namen vergessen haben und um 23 Uhr den Nachfassplan brauchen.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[Das vollständige Star-History-Diagramm ansehen](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Übersetzungen

Die README gibt es in 12 Sprachen, die Oberfläche der Website ebenso. Englisch ist der Referenztext.

- [中文](README.md) (Chinesisch, vollständig)
- [Español](README_ES.md) (Spanisch, Einstiegsfassung, Korrekturleser gesucht)
- [Português](README_PT.md) (Brasilianisches Portugiesisch, vollständig)
- [Français](README_FR.md) (Französisch, vollständig)
- [العربية](README_AR.md) (Arabisch, vollständig, RTL)
- [Русский](README_RU.md) (Russisch, vollständig)
- [Deutsch](README_DE.md) (vollständige deutsche Fassung – diese Datei)
- [日本語](README_JA.md) (Japanisch, vollständig)
- [한국어](README_KO.md) (Koreanisch, vollständig)
- [Türkçe](README_TR.md) (Türkisch, vollständig)
- [Bahasa Indonesia](README_ID.md) (Indonesisch, vollständig)

Die Etappen-Dokumente in `docs/` gibt es bisher nur auf Chinesisch. Übersetzen Sie jede Etappe, in der Sie sicher sind; behalten Sie die sechsteilige Struktur und gleichen Sie die Begriffe mit [GLOSSARY.md](GLOSSARY.md) ab. Muttersprachler, die eine README gegenlesen können, sind ebenfalls sehr willkommen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Lizenz

[MIT](LICENSE) © 2026 zero-to-trade contributors

Nutzen Sie es, ändern Sie es, verkaufen Sie damit. Behalten Sie den Hinweis auf die Urheber. Ein Vorbehalt: Nichts hiervon garantiert Ihnen einen Abschluss. Garantiert ist nur, dass Sie nicht stecken bleiben, weil Sie den nächsten Schritt nicht kennen.

---

## Fragen & Beiträge

**Eröffnen Sie ein Issue: https://github.com/6hn68/zero-to-trade/issues**

Ist hier etwas falsch? Sagen Sie es, das zählt als Beitrag. Sie verkaufen in einen Markt, von dem dieses Repo noch nie gehört hat? Das ist ein PR, den ich wirklich haben will. Sie halten die ganze Methode für falsch? Streiten Sie mit mir in einem Issue – ich liege lieber laut daneben.

Keine Autorenbiografie, mit Absicht. **Überzeugen soll der Inhalt, nicht wer ihn geschrieben hat.** Wenn Sie mich erreichen müssen: Erwähnen Sie den Maintainer mit @ in einem Issue, oder hinterlassen Sie eine Nachricht über das Formular unten auf der Website. So oder so erreicht sie den Autor.
