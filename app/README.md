# Lokale Paket-Sortierlogik

Soll: Pakete für Berlin gehen an Station `berlin`, für Hamburg an `hamburg`,
für München an `munich`. Die Paket-ID beeinflusst das Ziel nicht.
Diese erste Version verarbeitet typisierte Pakete mit diesen drei Zielen;
unbekannte Ziele, PLZ-Zuordnung, Gewichte und Expressregeln sind nicht Teil
dieses Schritts. Es gibt keine externe Eingabeschnittstelle.

`src/routing.ts` ist der funktionierende Ausgangsstand. `src/parcels.ts` enthält
sechs feste Demopakete; `src/demo.ts` gibt tatsächliche Routingergebnisse als
JSON aus. Die Anwendung hat keine Laufzeitabhängigkeiten. Für Typprüfung und
Build wird TypeScript 7.0.2 als Entwicklungsabhängigkeit aus der eigenen
`package-lock.json` installiert. Node 24 kann die Quelldateien auch direkt ausführen.

Auf diesem Mac zunächst im Repository-Root:

```bash
export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
cd app
npm ci --ignore-scripts --no-audit --no-fund
npm run typecheck
npm run demo
npm test
npm run build
npm run verify:artifacts
```

Die Tests haben einen eigenen fachlichen Erwartungskatalog mit sechs Paketen
(zwei je Ziel, andere IDs als in der Demo). Sie lesen keine Routingtabelle aus
der Implementierung. Derselbe Testvertrag wird gegen beide Varianten ausgeführt;
es gibt keine erwartete Fehlerausnahme und keine Umkehrung des Testergebnisses.
Die Eingabeobjekte sind eingefroren. Das ist lokale fachliche Verifikation;
eine Isolation gegen absichtlich manipulativen Fremdcode ist noch nicht aufgebaut.

## Reproduzierbarer Routingfehler

`scenarios/berlin-to-hamburg/routing.ts` ist eine separate, absichtlich fehlerhafte
Implementierung: nur die Berliner Route ist auf `hamburg` geändert. Weder
Produktionsdatei noch fachliche Erwartungen werden dafür umgeschrieben.

```bash
npm run demo:scenario
npm run test:scenario
```

`test:scenario` muss mit Exitcode 1 scheitern: zwei Berliner Fälle liefern
`hamburg` statt `berlin`; Hamburg und München bleiben korrekt. `npm test`
prüft ausdrücklich nur den funktionierenden Stand. Ein allgemeiner
`node --test`-Aufruf kann auch die absichtlich rote Szenariosuite entdecken.

## Build und vorbereitete GitHub-Workflows

`npm run typecheck` prüft Referenz und Routingfehlervariante. `npm run build`
entfernt vorher ausschließlich `app/dist/` und kompiliert nur `src/` dorthin.
Relative `.ts`-Importe werden zu `.js`; `node dist/demo.js` führt das Ergebnis aus.
Die App benötigt den Compiler unter `infra/` nicht mehr.

Die Workflows unter `../.github/workflows/` sind ausschließlich für einen
späteren manuellen Start (`workflow_dispatch`) vorbereitet. Kein Push-/PR-Trigger,
kein Deployment, AWS-Zugang oder Repository-Secret. Der übliche temporäre
GitHub-Token darf nur `contents: read`; Checkout speichert keine Credentials.
Der Artefaktupload verwendet den von GitHub bereitgestellten Laufzeit-Zugang.
Actions sind auf volle Commit-SHAs festgelegt; Node-Version ist 24.22.2.
Cache ist deaktiviert, Joblimit fünf Minuten, Artefaktaufbewahrung ein Tag.

- `app-ci.yml`, Auswahl `reference`: `npm ci` → Typprüfung → fachliche Tests →
  Build → Prüfung aller drei erforderlichen JS-Dateien → Artefaktupload.
- `app-ci.yml`, Auswahl `routing-error`: dieselbe Typprüfung, dann
  `npm run test:scenario`. Der tatsächliche Testfehler beendet den Job vor dem
  Build/Upload; kein `continue-on-error` oder als Erfolg umgedeuteter Fehler.
- `app-pipeline-error.yml`: korrekte Anwendung, erfolgreiche Tests und Build,
  aber `ARTIFACT_PATH: app/build` statt `app/dist`. Dieselbe Variable steuert
  Prüfung und Upload. Die Artefaktprüfung scheitert; der Upload wird übersprungen.
  Beide Upload-Schritte setzen zusätzlich `if-no-files-found: error`.

Run-Schritte arbeiten standardmäßig in `app/`. Die Artefaktprüfung arbeitet
ausdrücklich im Repository-Root; Uploadpfade sind ebenfalls relativ zum Root.
Bei Erfolg wird nur `app/dist/` hochgeladen, nicht das Repository, die
Infrastruktur oder lokale Empfänger-/State-Dateien.

Beide Fehlermodi sind getrennt: Der Routingfehler ändert das fachliche Ergebnis,
der Pipelinefehler ausschließlich den erwarteten Artefaktpfad im echten Workflow.
Ein fehlgeschlagener Lauf veröffentlicht nichts. Ein Hosting/Deployment und damit
eine letzte online bereitgestellte Version existieren in diesem Schritt noch nicht.

Pipelinefehler vom Repository-Root lokal reproduzieren:

```bash
npm --prefix app run typecheck
npm --prefix app test
npm --prefix app run build
node app/scripts/verify-artifacts.mjs app/build
```

Der letzte Befehl muss mit Exitcode 1 scheitern, während `app/dist/` vorhanden
ist. Zum Vergleich besteht `node app/scripts/verify-artifacts.mjs app/dist`.
Der Prüfer verlangt `routing.js`, `parcels.js` und `demo.js` als nichtleere,
reguläre Dateien; fehlende, leere und unvollständige Ordner scheitern ebenfalls.

Lokal am 9. November 2026 geprüft: Installation aus Lockdatei, Typprüfung,
6/6 Referenztests, Build, kompilierte Demo und Artefaktprüfung erfolgreich;
Routingfehler 2/6 rot, falscher Pfad Exitcode 1. Beide Workflows bestehen
`actionlint` 1.7.7. Kein GitHub-Lauf/Upload durchgeführt; Runner-, Token- und
Uploadverhalten sind damit noch nicht praktisch auf GitHub nachgewiesen.

Quellen: [setup-node](https://github.com/actions/setup-node),
[Checkout](https://github.com/actions/checkout),
[Artefaktupload und fehlende Dateien](https://github.com/actions/upload-artifact#customization-if-no-files-are-found).
