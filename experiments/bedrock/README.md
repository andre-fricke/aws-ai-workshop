# Ein einzelner Reparaturvorschlag mit Bedrock

**Aktueller Stand:** Supportfall `179423481400635` laut André manuell eingereicht.
Bedrock-Inferenz bleibt bis zur Klärung blockiert. Nächster Schritt ist die
Prüfung der AWS-Antwort im bestehenden Fall; keinen neuen Fall oder Modellversuch
aus diesem Dokument ableiten. AWS-Fallstatus und eingereichter Wortlaut wurden
nicht erneut ausgelesen. Details in [quota-request-draft.md](quota-request-draft.md).

Vorbereitung und Versuche vom 9. November 2026;
**noch keine erfolgreiche Inferenz**. Die erste freigegebene Tokenzählung scheiterte:
AWS meldet für Nova Lite `The provided model doesn't support counting tokens.`
Damit war die Freigabebedingung von maximal 4.096 Eingabetokens nicht nachgewiesen;
es folgte damals kein `Converse` und keine Wiederholung. Nach einer neuen,
ausdrücklichen Freigabe ohne Tokenzählungsbedingung wurde genau ein direkter
`Converse`-Versuch ausgeführt; AWS lehnte ihn wegen des täglichen Tokenlimits ab.
Das Experiment erzeugt einen Vorschlag als JSON-Daten. Es gibt keine Agentenschleife,
Werkzeuge für das Modell, automatische Codeänderung, Testausführung der Modellantwort,
Fallbackmodelle oder automatische Inferenzwiederholungen.

## Lesend bestätigter Accountstand

**Ergänzung:** Die spätere Einzelprüfung unterscheidet modellbezogene Nullquoten
von **Cross-Model Max Tokens Per Day = 150.000.000** in Stockholm. Das
modellübergreifende Tageslimit ist nicht null. Werte, Änderbarkeit und ein
noch nicht abgesendeter Antragsentwurf stehen in
[quota-request-draft.md](quota-request-draft.md).

Profil `andre-ai-lab`, Region `eu-north-1`, erwarteter Account `331001679034`:

- `ListFoundationModels`: Nova Micro aktiv, in Stockholm nur `INFERENCE_PROFILE`.
- `GetFoundationModelAvailability`: Micro und Lite jeweils `AUTHORIZED`,
  Agreement/Entitlement/Region jeweils `AVAILABLE`.
- `GetInferenceProfile` für `eu.amazon.nova-micro-v1:0`: aktiv; mögliche Ziele
  Frankfurt, Stockholm, Irland und Paris. Kein rein schwedischer Micro-Aufruf.
- `GetFoundationModel` für `amazon.nova-lite-v1:0`: aktiv, `ON_DEMAND` unterstützt.
- Service Quotas meldet für Lite direkte RPM (`L-E386A278`), TPM
  (`L-70423BF8`) und tägliche Tokens (`L-45E0AD92`) jeweils **0**.
  Auch die gelesenen Micro-/Nova-2-Lite-Inferenzquoten stehen auf 0.
- Python-SDK mit bestehendem Loginprofil per STS und Bedrock-/Quoten-Lesezugriff
  erfolgreich geprüft; kein zusätzlicher Credential-Process und keine festen Keys.

**Inferenz noch nicht nachgewiesen und derzeit nicht als einsatzbereit bewertet.**
Modellkatalog, Modellberechtigung, Quoten und ein erfolgreicher Runtime-Aufruf
sind unterschiedliche Nachweise. Vor Inferenz die Nullquoten klären; das Script
bricht bei weiterhin gemeldeter Nullquote ab. Es beantragt keine Quotenänderung,
wechselt weder Region noch Accountplan und erstellt keine Ressourcen.

## Empfehlung und Kosten vor Freigabe

Für diesen kurzen TypeScript-Fall: **Nova Lite V1**, direkte On-Demand-Inferenz
mit `amazon.nova-lite-v1:0` am Stockholm-Runtime-Endpunkt. So bleibt die Inferenz
in `eu-north-1`; kein Cross-Region-Profil oder automatisches Regional-Fallback.
Die Eignung für genau diese Reparatur ist eine begründete Versuchsauswahl,
noch kein gemessener Reparaturerfolg. Micro ist kleiner/günstiger positioniert,
erfordert hier aber die oben genannten möglichen EU-Zielregionen.

Offizielle AWS Price List API, gelesen am 9. November 2026 für **Nova Lite,
Stockholm, On-demand Inference** (Preisstand gültig ab 1. November 2026):

| Position | USD je 1.000 Tokens | USD je 1 Mio. Tokens |
|---|---:|---:|
| Eingabe | 0,000065 | 0,065 |
| Ausgabe | 0,00026 | 0,26 |

SKU Eingabe: `5B2T2U8FNRYYV6G4`, Ausgabe: `E4Z3PKDHV45PZQMB`.
Preislisten-Version: `20261106184538`. Kein Batch, Caching oder Provisioned Throughput.
Guthaben wird in dieser Verbrauchsrechnung nicht abgezogen; Preise vor Steuern.

- Modellgrenzen laut AWS: 300K Kontexttokens, maximal 10K Ausgabetokens.
- Grenzen dieses Versuchs: Request maximal **12.000 UTF-8-Bytes**, höchstens
  **4.096 Eingabetokens** nach kostenloser `CountTokens`-Prüfung und **512 Ausgabetokens**.
- Der vorbereitete Request umfasst **2.903 UTF-8-Bytes**. Dies ist keine Tokenzählung.
  Die erste echte `CountTokens`-Anfrage wurde abgelehnt (siehe Nachweis unten).
  Die bisher vorbereitete Tokenzählung ist für dieses Modell daher nicht nutzbar.
- Maximaler kalkulierter Tokenpreis innerhalb dieser Grenzen:
  `(4096 × 0,000065 + 512 × 0,00026) / 1000 = 0,00039936 USD` für einen Aufruf.
  Die tatsächlichen Zähler werden aus der Antwort dokumentiert. Der Versuch
  umfasst maximal eine SDK-Inferenzanfrage mit deaktivierten SDK-Retries.

Nova Lite unterstützt laut AWS **keine nativen Structured Outputs**. JSON wird
deshalb per Prompt verlangt und anschließend lokal strikt validiert; das Modell
kann ungültiges JSON liefern. Dies löst keinen zweiten Aufruf aus.

## Kontext und Validierung

Übermittelt würden ausschließlich:

1. `context/requirements.md`: drei Zielstationen, ID-unabhängiges Routing und Grenzen.
2. Die fehlerhafte `app/scenarios/berlin-to-hamburg/routing.ts` mit SHA-256.
3. `context/test-log-excerpt.txt`: kuratiertes Fragment aus dem tatsächlichen
   Routingfehlerlauf auf `e7577b1`, mit Link und Herkunft. Kein kompletter Logdownload.

Die korrekte Implementierung, vollständige Testdateien, AWS-Konfiguration,
Budgetempfänger und Credentials werden nicht in den Prompt aufgenommen.
Logs und Quellcode sind als untrusted data markiert.

Erwartetes JSON: `schema_version`, `target_path`, `source_sha256`, `diagnosis`,
`change: {old, new}`. Der Validator verwirft Zusatzfelder, doppelte JSON-Schlüssel,
Markdown, falsche Pfade/Hashes, zu große Antworten, abgebrochene Ausgaben,
Tool-Anforderungen und Änderungen außerhalb des Stationsliterals im Berliner Zweig.
Es wird kein Patch geschrieben oder ausgeführt. Auch ein strukturell zulässiger
Vorschlag kann fachlich falsch sein: unabhängige Tests wären ein späterer Schritt.
Synthetische Vorschläge in den lokalen Validatortests sind keine Modellantworten.

## Befehle vom Repository-Root

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r experiments/bedrock/requirements.txt
.venv/bin/python -m unittest discover -s experiments/bedrock -p 'test_*.py'
```

Offline vorbereiten (bereits ausgeführt; überschreibt vorhandene Dateien nicht):

```bash
.venv/bin/python experiments/bedrock/propose.py prepare
```

Lesende SDK-Prüfung (bereits ausgeführt; keine Inferenz oder Promptübertragung):

```bash
.venv/bin/python experiments/bedrock/propose.py inspect
```

**Der unten vorbereitete Ablauf ist derzeit blockiert:** Neben den Nullquoten
ist auch die fehlende `CountTokens`-Unterstützung zu klären. Der folgende Befehl
ist keine Aufforderung zu einem neuen Versuch und darf mit der vorhandenen
Freigabe nicht erneut ausgeführt werden:

```bash
.venv/bin/python experiments/bedrock/propose.py invoke --approved
```

Dieser Befehl prüft erneut Identität, Modellzugang, Quoten und Übereinstimmung des
gespeicherten Requests mit dem Kontext; danach kostenlose Tokenzählung und
höchstens ein `Converse`. Bei Fehler kein Retry und kein Modellwechsel.
`attempt.json` verhindert eine weitere Inferenz im selben Laufverzeichnis.
Bei Timeout könnte AWS die erste Anfrage bereits verarbeitet haben; nicht
einfach erneut starten. Fehler und Rohantwort gemeinsam beurteilen.

Alle Laufdateien liegen vertraulich und Git-ignoriert unter `runs/bedrock-routing/`:
Request, Versuchsnachweis, Rohantwort, Metriken und gegebenenfalls validierter
Vorschlag. Metriken enthalten Modell-/Promptversion, Hash, Dauer, Request-ID,
Stopgrund, Tokenverbrauch und berechneten Tokenpreis. Ungültige Antworten bleiben
als Rohantwort erhalten, gelten aber nicht als akzeptierter Vorschlag.

Minimaler späterer Runtime-Zugang: `bedrock:InvokeModel` und `bedrock:CountTokens`
auf `arn:aws:bedrock:eu-north-1::foundation-model/amazon.nova-lite-v1:0`;
zusätzlich die verwendeten Identitäts-/Modell-/Quoten-Leserechte. Keine IAM-
Änderungen oder neuen Berechtigungen durch dieses Experiment.

## Tatsächlicher API-Ablauf nach Freigabe

Der Nutzer gab zuerst Tokenzählung und nur bei nachgewiesenen höchstens 4.096
Eingabetokens genau einen direkten Nova-Lite-Inferenzversuch in Stockholm frei,
maximal 512 Ausgabetokens, unter 0,001 USD erwarteten Inferenzkosten, ohne Retries.
Die gemeldeten Nullquoten blieben dabei reine Diagnose; keine Quote wurde geändert.

1. Gespeicherten Request mit dem vorbereiteten Kontext verglichen: unverändert.
2. Bestehendes Loginprofil über Boto3/CRT genutzt; `STS.GetCallerIdentity`
   bestätigte den erwarteten Account. Keine Credentials protokolliert.
3. Bedrock-Runtime-Client: `https://bedrock-runtime.eu-north-1.amazonaws.com`,
   `retries={total_max_attempts: 1, mode: standard}` (keine SDK-Retries).
4. Genau ein `CountTokens(modelId='amazon.nova-lite-v1:0', input={converse:
   {system: ..., messages: ...}})` mit dem gespeicherten System-/Benutzerkontext.
5. HTTP 400, `ValidationException`, AWS-Meldung wörtlich:
   `The provided model doesn't support counting tokens.`
   Request-ID `717235ba-3290-4c8e-8181-ebce75b24560`, `RetryAttempts=0`.
6. Abbruch: keine Tokenzahl, kein `Converse`, keine Modellantwort, keine
   Vorschlagsvalidierung und keine Reparaturanwendung. Keine Inferenzkosten.

Lokaler Nachweis: `runs/bedrock-routing/request.json`, `count-attempt.json` und
`count-error.json`; alle Git-ignoriert. Quellhash der übermittelten fehlerhaften Datei:
`ff8c4909e0d2592f2932b9f9880b20d5870141704b7874f1d2532a24d16298ad`.
Die Angabe von 2.903 Bytes ersetzt keine modellgenaue Tokenzählung. Es wurde kein
anderer Tokenizer, Modell-, Regions- oder Inferenzfallback verwendet.

## Einzelner Converse-Versuch mit neuer Freigabe

Der Nutzer entfernte anschließend ausdrücklich die Bedingung von 4.096
gezählten Eingabetokens und genehmigte genau den unveränderten Request,
maximal 12.000 UTF-8-Bytes und 512 Ausgabetokens, ohne CountTokens oder Retries.

- Request mit vorbereitetem Kontext und Hash aus dem ersten Versuch verglichen:
  unverändert. Gespeicherte JSON-Datei 3.008 Bytes; kompakte Darstellung
  2.903 Bytes; tatsächlich versendeter HTTP-Body **2.938 Bytes**.
- Modell `amazon.nova-lite-v1:0`, direkter Runtime-Endpunkt
  `https://bedrock-runtime.eu-north-1.amazonaws.com`, kein Inferenzprofil.
- Identität mit bestehendem Profil bestätigt. SDK `total_max_attempts=1`;
  zusätzlich tatsächliche HTTP-Sendeversuche gezählt: **1**, `RetryAttempts=0`.
- Genau ein `Converse`, `maxTokens=512`, Temperatur 0, kein CountTokens.
- Antwort: **HTTP 429 / ThrottlingException**. AWS-Meldung wörtlich:
  `Too many tokens per day, please wait before trying again.`
- Request-ID: `ebd73222-fedd-4d96-941a-3f821a3b3f1e`.
- Keine Modellantwort oder Usage-Zähler zurückgegeben; deshalb keine
  Berechnung tatsächlicher Tokenkosten möglich. Dies ist kein gemessener
  erfolgreicher Inferenzlauf und keine Kostenmessung mit Nullverbrauch.
- Kein Vorschlag vorhanden, deshalb keine Vorschlagsvalidierung oder
  Reparaturanwendung. Kein Retry, Fallback, Upgrade oder Quotenänderungsantrag.

Nachweise lokal unter `runs/bedrock-routing/attempt.json` und
`inference-error.json` (Git-ignoriert). Die einmalige Freigabe ist verbraucht;
kein weiterer Aufruf aus diesem Ergebnis ableiten.

## Quellen

- [Nova Lite: Grenzen, Regionen, fehlende native Structured Outputs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-lite.html)
- [Nova Micro und EU-Inferenzregionen](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-micro.html)
- [AWS Bedrock Preise](https://aws.amazon.com/bedrock/pricing/)
- [AWS Price List GetProducts](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_pricing_GetProducts.html)
- [Kostenlose Tokenzählung](https://docs.aws.amazon.com/bedrock/latest/userguide/count-tokens.html)
- [Converse und InvokeModel-Berechtigung](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
- [Boto3-Loginprofil mit CRT](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html#login-with-aws-cli)
