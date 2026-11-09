# AWS-KI-Workshop: Paket-Sortieranlage mit selbstständiger KI-Reparatur

Für André Fricke · Stand: 6. November 2026

## Ziel

Wir bauen eine öffentliche interaktive Referenz für Andrés Homepage: eine animierte Paket-Sortieranlage mit einer echten GitHub-Actions-Pipeline und einem KI-Reparaturagenten. Besucher können vorbereitete Fehler auswählen oder begrenzte Teile des Codes selbst bearbeiten. Zwei Modi gehören zum fertigen Ziel:

1. **Anwendung kaputt:** Pakete werden falsch sortiert; unabhängige Tests erkennen den Logikfehler.
2. **Pipeline kaputt:** Die Anwendung ist korrekt; ein falscher Artefaktpfad verhindert die Bereitstellung.

Der Agent untersucht den Fehler, erstellt ein Ticket, erarbeitet eine Reparatur als echten GitHub-Pull-Request und lässt sie unabhängig prüfen. Nach erfolgreicher automatischer Freigabe und Merge wird das geprüfte Ergebnis bereitgestellt. Ein Reparaturbericht wird ergänzt und das Ticket abgeschlossen. Bei Misserfolg bleiben Ticket und Bericht mit offenen Punkten bestehen.

Die Website zeigt Simulation, Pipeline, Ticket, tatsächliche Werkzeugaufrufe, Logs, Diffs, PR-/Prüfstatus und Dokumentation. Eine Architekturansicht erklärt den Aufbau. Kein Chatfenster als Kernprodukt und keine bloße Animation einer vorab festgelegten Reparatur.

Lernziel: André kann das mit KI-Unterstützung aufgebaute System erklären, betreiben, gezielt ändern und Fehler eingrenzen. Schwerpunkt sind Modellintegration, Kontextaufbereitung, Werkzeuge, Grenzen, Evaluation und Betrieb. Programmieren und DevOps bringt André bereits mit; manuelles Schreiben des Codes ist kein Lernziel. Die Referenz ist als Eigenprojekt gekennzeichnet; sie ersetzt keine produktive Kundenreferenz.

## Verbindliche Entscheidungen

- Eigenständiges bestehendes Repository `/Users/mainuser/git/aws-ai-workshop`; Homepage bleibt separat. Entscheidung: Repository öffentlich als einsehbare Referenz mit Code, echten PRs und Pipeline-Läufen. Tatsächliche GitHub-Sichtbarkeit vor einer Änderung prüfen; die Dokumentationsänderung selbst veröffentlicht nichts. Keine Kundendaten oder Credentials versionieren. Besuchereingaben, die in Branches/PRs/Logs erscheinen, sind öffentlich; darauf im Editor vor dem Absenden klar hinweisen.
- **GitHub Actions** übernimmt Build, Tests und Pipelineablauf einschließlich Reparaturintegration. CodeBuild und Step Functions sind nicht Bestandteil des Grundentwurfs.
- **AWS CDK mit TypeScript** verwaltet Anwendungsinfrastruktur, Rollen und Monitoring in Stockholm. **Terraform verwaltet ausschließlich das globale AWS-Budget** über die Budgets-API in `us-east-1`; keine CloudFormation-Bereitstellung dort. Budget und Anwendung haben getrennte Zustände; keine Ressource doppelt verwalten. Terraform und Programmierung sind bereits beherrscht. TypeScript/CDK bleibt gewählt; dessen AWS-spezifische Arbeitsweise wird am generierten Ergebnis nachvollzogen, ohne einen allgemeinen Programmierkurs einzubauen.
- AWS ausschließlich über IaC verwalten. GitHub-/Atlassian-Konfiguration ebenfalls als versionierte Konfiguration automatisieren, soweit sinnvoll unterstützt. CDK deckt diese externen Produkte nicht automatisch ab; nötige Accountregistrierungen und nicht automatisierbare Schritte gesondert erklären und abstimmen.
- **VS Code + Codex** als Entwicklungsumgebung und Coach. Andrés vorhandenen ChatGPT-Zugang nutzen; Entwicklungsassistenz und Modellzugang der veröffentlichten Anwendung sind getrennte Entscheidungen und Kostenstellen. Keine Weitergabe persönlicher Codex-Zugänge an Websitebesucher.
- TypeScript für Simulation und Weboberfläche; Python zunächst für Agent und KI-Evaluation; Amazon Bedrock als Modellzugang.
- Region **Stockholm (`eu-north-1`)**, vorhandener Free plan. Kein Wechsel nach Frankfurt oder Upgrade allein für diesen Plan.
- Besucher **ohne GitHub- oder Atlassian-Anmeldung**, ohne Repositoryrechte. Ein Backend vermittelt die begrenzten Aktionen; Zugangstokens bleiben serverseitig.
- Echte Reparatur-PRs, automatischer Demo-Freigabemodus und anschließendes Deployment. Der alternative menschliche Freigabemodus wird sichtbar erklärt und später praktisch ergänzt.
- Tickets und Dokumentation gehören zum Ziel. Echte **Jira-/Confluence-Anbindung** ist die gewählte Richtung; Free-plan-Berechtigungen und aktuelle Grenzen vor Einrichtung prüfen. Zunächst lokale Adapter/Ansichten aufbauen, anschließend reale APIs anbinden und dies ehrlich kennzeichnen.
- **20 USD monatlich als Kostenziel, maximal 50 USD monatliche Zahlungsbereitschaft**, AWS und GitHub zusammen betrachten. Das ist keine bestehende harte Kostensperre. Nutzung und Preise vor öffentlicher Freigabe messen und kalkulieren.
- Separate Subdomain, etwa `lab.andre-fricke.de`, und verlinkte Fallstudie auf der Homepage bevorzugt. iframe optional nach Prüfung von Homepage, Layout und Einbettungsregeln.
- Kleine vertikale Schritte: lokal → echte GitHub-Pipeline → erster geprüfter Reparaturablauf → PR/Merge/Deployment → Integrationen → öffentliche Oberfläche. Beide Fehlerklassen und beide Eingabearten gehören zum Abschlussziel, nicht zwingend zum allerersten Prototyp.

## Noch offene Technologieentscheidungen

React mit Vite, Lambda/API Gateway, GitHub App, S3 und gegebenenfalls DynamoDB sind Vorschläge, noch keine vollständig beschlossene oder geprüfte Architektur. Offen sind Modell, genaue Agentenlaufzeit, Hosting/Preview-Isolation und Speicher. Polling, Docker-Sandbox auf frischer GitHub-VM sowie zwei getrennte GitHub Apps sind als Entwurf gewählt und müssen praktisch validiert werden. Der Agent soll zunächst möglichst direkt in GitHub Actions ausführbar sein; ein eigener Dienst ist erst bei begründetem Bedarf nötig.

Für die erste Werkzeugschleife kein Framework voraussetzen. Authentifizierung zwischen GitHub und AWS bevorzugt über OIDC, sofern im Account unterstützt. GitHub-App-Authentifizierung für serverseitige GitHub-Aktionen prüfen. Keine Tokens im Browser und keine pauschale Freigabe des Repositorys.

## Umfang und überprüfbare Zwischenziele

Dies ist ein mehrstufigiges Lern- und Referenzprojekt, kein kleiner Workshop für einen Nachmittag. Der erste erfolgreiche KI-Aufruf und eine geprüfte Reparatur sollen früh gelingen; Website, automatische Freigabe und Atlassian werden danach ergänzt. Keine Termine oder Gesamtkosten versprechen, bevor ein vollständiger Beispielablauf gemessen wurde.

| Zwischenziel | Beobachtbarer Abschluss |
|---|---|
| 1. Lokaler Lernerfolg | Beide Fehler reproduzierbar; ein Modell schlägt einen erlaubten Patch vor, unabhängige Prüfung bestätigt dessen Wirkung |
| 2. Privater Ablauf auf GitHub | Ein vollständiger Lauf mit echter Pipeline, PR, überprüfter Freigabe und isoliertem Preview; zunächst nur durch André gestartet |
| 3. Nachvollziehbare Referenz | Beide Modi, Ticket/Bericht und sichtbare Belege; Architektur und Grenzen erklärt |
| 4. Öffentliche Demo | Anonyme Eingaben, Missbrauchsgrenzen, Isolation, Cleanup und Kostenmessung bestehen die Veröffentlichungskriterien |

Die Etappen unten sind Lernmodule, keine starre Reihenfolge: technische Machbarkeitsprüfungen früh vorziehen. RAG bleibt eine geplante Vertiefung, blockiert aber weder die erste Reparatur noch die erste Demo. Alle Ausbauideen bleiben im Backlog erhalten.

## Frühe Machbarkeitsprüfungen vor größerem Ausbau

Nicht alle Details sind bereits bewiesen. Für jeden Versuch Ergebnis und Konsequenz kurz im Repository dokumentieren; bei einem Hindernis zuerst den Entwurf korrigieren.

1. **Account und Modell:** CDK-/Python-SDK-Anmeldung, tatsächlicher Bedrock-Aufruf in Stockholm und ein benötigter AWS-Bereitstellungsweg funktionieren im bestehenden Account. CLI-Login und Modellkatalog reichen als Nachweis nicht aus. Vor kostenintensiven Versuchen Preis und Limits prüfen.
2. **GitHub-Freigabe:** Minimalen Test-PR mit den zwei App-Identitäten anlegen. Beweisen, dass Approval zählt, der vorgeschriebene Check nur aus der erwarteten Quelle akzeptiert wird, neue Commits erneut geprüft werden und Auto-Merge funktioniert. Branch-Erstellung und spätere Löschung mit Rulesets separat testen. Ohne Nachweis keine automatische Freigabe versprechen; Abweichungen gemeinsam entscheiden.
3. **Vertrauenswürdige Steuerung:** Festlegen, aus welchem unveränderlichen Commit jeder steuernde Workflow und Prüfcode geladen wird. GitHub-App-Rechte sind keine automatische Beschränkung auf einzelne Branches oder Dateien. Vermittlungsdienst und Branchregeln müssen diese Grenzen erzwingen; die Verification App darf keine PR-Inhalte als eigene Steuerung ausführen. Falls dies im Projekt-Repository nicht sauber isolierbar ist, ein zusätzliches reines Demo-Repository vorsehen. Homepage bleibt in jedem Fall separat.
4. **Reparatur einer echten Pipeline:** Einen erlaubten Artefaktpfad im Demo-Workflow ändern und wirklich auf GitHub ausführen. Genau definieren, welcher Workflow von welchem Ref startet und wie dessen Fehler den vertrauenswürdigen Agenten auslöst. Keine impliziten Folgeevents oder automatische Wiederholungen voraussetzen; Workflow-Schreibrechte nur im validierenden Vermittlungsdienst.
5. **Sandbox und Testaussage:** Einen fehlerhaften sowie absichtlich manipulativen Besucherstand isoliert ausführen. Der vertrauenswürdige Prüfer muss erwartete Ergebnisse selbst vergleichen; eine vom Besuchercode ausgegebene Meldung „Tests grün“ oder ein gefälschter Ergebnisreport zählt nicht. Schreibgeschützte Tests im selben Prozess wie fremder Code allein sind kein hinreichender Vertrauensnachweis.
6. **Kosten und Laufzeit:** Einen vollständigen Lauf mit Wartezeiten, Modellaufrufen, Artefakten und Cleanup messen. Daraus Kontingente und eine Monatsrechnung für beispielhafte Besucherzahlen ableiten, getrennt nach laufenden und nutzungsabhängigen Kosten. Erst dann über öffentliche Live-Nutzung entscheiden.

## Fachlicher Auftrag der Paket-Sortieranlage

Erste Version: links ankommende Pakete, Förderbänder und drei Zielstationen Berlin, Hamburg und München. Eine TypeScript-Routingfunktion bestimmt das Ziel. Feste Beispieldaten und geschützte Tests definieren das richtige Verhalten. Die Animation verwendet tatsächliche Routingergebnisse und zählt richtige/falsche Zustellungen.

Besucher können einen Fehler aktivieren oder die freigegebene Routingfunktion im Editor ändern. Der Auftrag bleibt gleich: die fachlichen Regeln wieder erfüllen. Das Modell soll anhand von Anforderungen, Implementierung und Testergebnissen reparieren; kein fest eingebauter Rücksetzmechanismus als KI-Erfolg ausgeben.

Für sofortige Vorschau beliebig veränderten Codes ist ein eigenes Sandbox-Konzept erforderlich. Bis dahin nur die zuletzt isoliert berechneten Ergebnisse anzeigen. Auch veröffentlichte Besucheranwendungen benötigen eine von Leitstand und Homepage getrennte Origin ohne gemeinsame Credentials; ein Pfad je Lauf allein isoliert aktiven Browsercode nicht.

## Zwei Fehlerklassen im fertigen Produkt

| Modus | Erstes Szenario | Sichtbares Verhalten | Erfolgskriterium |
|---|---|---|---|
| Anwendung kaputt | Berlin-Pakete gehen zur Hamburger Station | Falsche Sortierung; Tests scheitern | Erlaubter Anwendungspatch besteht unabhängige Tests |
| Pipeline kaputt | Workflow erwartet `app/build/`, Build erzeugt `app/dist/` | Build und Tests erfolgreich, Artefaktprüfung scheitert, kein neues Deployment | Erlaubte Pfadkorrektur liefert tatsächlich die erwarteten geprüften Dateien |

Beim Pipelinefehler bleibt eine letzte funktionierende Version sichtbar. Zeige ausdrücklich, dass sie unverändert ist und die neue Version noch nicht bereitgestellt wurde. Ein fehlender Artefaktpfad muss im Demo-Workflow wirklich einen Fehler auslösen; eine bloße Upload-Warnung zählt nicht als fehlgeschlagene Pipeline.

Weitere vorbereitete Fehler sind im Ausbauplan festgehalten. Im Pipeline-Editor ausschließlich definierte Felder eines tatsächlichen Demo-Workflowabschnitts bearbeiten lassen, zunächst den Artefaktpfad. Freie YAML-/Shelländerungen gehören nicht zum öffentlichen Editor. Die unabhängige Reparaturprüfung und privilegierte Automatisierung liegen außerhalb dieses bearbeitbaren Bereichs.

## Arbeitsweise: KI-gestützt aufbauen und verstehen

Der Workshop folgt Andrés tatsächlicher beruflicher Arbeitsweise mit KI-Unterstützung. Codex soll Implementierung und Routinearbeiten übernehmen. André muss weder Anwendung noch Infrastruktur selbst schreiben und keinen Code abtippen. Langsam bedeutet verständliche, überschaubare Schritte und gezielte Erklärungen; es bedeutet nicht, jede Datei oder jeden einzelnen Befehl manuell abzuarbeiten.

| Codex übernimmt | André steuert und versteht |
|---|---|
| Anwendung, UI, CDK, Workflows und Integrationscode generieren | Zielverhalten, Architekturentscheidungen und Zusammenspiel der Komponenten |
| Sinnvolle Tests, Beispieldaten und Fehlerfälle erstellen und ausführen | Ob Anforderungen und unabhängige Erfolgskriterien sinnvoll geprüft werden |
| Lokale Builds, Synthese und andere Routineprüfungen ausführen | Relevante Änderungen, Berechtigungen, Kosten und Ergebnisse beurteilen |
| Logs untersuchen, Reparaturen vorschlagen und Dokumentation aktualisieren | Diagnose nachvollziehen, Entscheidungen treffen und Grenzen erkennen |

Diese Aufteilung gilt für alle Etappen, auch wenn dort „bauen“, „anlegen“, „ergänzen“ oder „prüfen“ steht. Codex darf passende zusammenhängende Änderungen erzeugen und lokal verifizieren. Generierte Tests sind nicht automatisch fachlich unabhängig: Sollverhalten und geschützte Verifikation gesondert beurteilen.

Pro Arbeitsrunde: kleines funktionierendes Ergebnis und Zweck nennen → Codex erzeugt und prüft die Umsetzung → relevante Änderungen knapp erklären → gemeinsam aufsetzen und Verhalten beobachten → bei einem neuen Zusammenhang gezielt eine Änderung oder Störung ausprobieren.

- Jeweils einen überschaubaren funktionierenden Abschnitt bearbeiten. Keine gesamte Anwendung auf einmal erzeugen, aber auch nicht für jeden Routinebefehl eine neue Gesprächsrunde verlangen.
- Wenn André einen Schritt selbst ausführt oder ein Ergebnis liefern muss, vor dem davon abhängigen Schritt warten. Verfügbare lokale Prüfungen selbst ausführen und zusammengefasst berichten.
- Bekannte Programmier-, Git-, Test- und DevOps-Grundlagen nur bei konkretem Bedarf erklären. Keine obligatorische zeilenweise CDK-/TypeScript-Einführung; kurze Einordnung von Einstiegspunkt, Stack und erzeugter Vorlage reicht zunächst.
- Neue KI-Zusammenhänge gezielt vertiefen: Kontext und Prompt, strukturierte Ausgaben, Tool-Schema und Rechte, Agentenschleife, unabhängige Verifikation, Evaluation, Fehlerbehandlung und Verbrauch. Nachvollziehbare Experimente statt abstrakter Theorieblöcke.
- Verständnis anhand des laufenden Systems prüfen: André erklärt beispielsweise, warum ein Werkzeug aufgerufen wurde, welcher Kontext fehlte oder warum eine Reparatur abgelehnt wird. KI-Nutzung bei Änderungen und Fehlersuche bleibt ausdrücklich erlaubt.
- Voraussetzungen und Dienstverfügbarkeit prüfen, bevor Installationen oder Architekturwechsel vorgeschlagen werden.
- Die Console zum Lesen und Kontrollieren nutzen. Infrastrukturänderungen gehören in IaC; CLI und SDK für lesende Prüfungen und Anwendungsaufrufe verwenden.
- Anmeldung, Verifizierung, MFA und andere persönliche Schritte erklären und separat dokumentieren. Nicht automatisierbare Änderungen gemeinsam abstimmen.
- Vor Deployments konkrete Ressourcen, Berechtigungen und erwartete Kosten erläutern. Lokale `infra/AGENTS.md` beachten; keine automatischen Deployments, Commits oder Pushes voraussetzen. Eine bereits erteilte konkrete Freigabe nicht für jeden Teilschritt erneut abfragen.
- Erfolge nur anhand beobachteter Ergebnisse dokumentieren. Eine vorgeschlagene Reparatur ist noch keine erfolgreiche Reparatur.

## Vorläufige Aufwandserwartung

Mit KI-generiertem Code und automatisierten Routineprüfungen grob **12–24 aktive Arbeitsstunden für eine erste vorzeigbare Demo** und **40–80 Stunden insgesamt für den vollständigen vereinbarten Zielumfang** ansetzen. Dies sind vorläufige Planungsspannen, keine Zusagen oder festen Workshopzeiten. Gemeinsame Erklärung und Fehlersuche sind enthalten; optionale Ausbauideen kommen hinzu. Wartezeiten auf externe Freischaltungen können die Kalenderdauer verlängern.

Erste Demo bedeutet ein vorbereitetes Fehlerszenario, echte GitHub-Pipeline, Reparatur-PR und einfache animierte Darstellung, zunächst nur von André gestartet. Der vollständige Umfang ergänzt beide Modi, anonyme Nutzung, begrenzten Code-Editor mit validierter Isolation, automatische Freigabe/Deployment, Jira/Confluence und Betriebsgrenzen. Generierung spart Implementierungszeit; Integrationsprobleme und Isolation fremden Codes müssen trotzdem praktisch gelöst werden. Nach dem ersten vollständigen Reparaturablauf die Spannen anhand tatsächlicher Arbeit neu einschätzen, ohne vereinbarte Funktionen stillschweigend zu streichen.

## Aktueller Einrichtungsstand

Bestätigt beziehungsweise lokal geprüft am 6. November 2026:

- Repository zunächst in Kiro geöffnet; anschließend VS Code + Codex als Entwicklungsumgebung gewählt. Öffnen und Anmeldung dort noch gemeinsam bestätigen. Homepage-Code liegt separat.
- Neues AWS-Projekt **Blank Canvas**, Anmeldung über Builder ID.
- Console zeigte Free plan, 100 USD Startguthaben und Ablauf am 6. Mai 2027. Aktuellen Guthabenstand später erneut prüfen.
- AWS CLI 2.39.5 über Homebrew installiert.
- Profil `andre-ai-lab`; `aws login` und `aws sts get-caller-identity` waren erfolgreich. Rolle: `AccountFullAccessRole`.
- Projektregion in AWS Settings und CLI-Standardregion als `eu-north-1` bestätigt.
- Bedrock-Modellkatalog gelesen; unter anderem Nova Micro, Nova Lite und Titan Text Embeddings V2 gelistet. Ein Modellaufruf ist noch nicht bestätigt.
- Node.js 24.22.2 über Homebrew zusätzlich installiert und im verwendeten Terminal aktiviert. Die PATH-Änderung gilt nur für dieses Terminal:

  ```bash
  export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
  ```

- CDK CLI 2.1148.0 installiert und aufgerufen.
- TypeScript-CDK-Grundgerüst unter `infra/` vorhanden, einschließlich `package.json`, Paket-Lockdatei, `bin/`, `lib/`, `test/` und `AGENTS.md`. Der Anwendungsstack enthält noch keine aktiven Ressourcen; der vorübergehende CDK-Budgetentwurf wurde durch Terraform ersetzt.
- Console-Budgetformular vorbereitet; Erstellung nicht bestätigt. Das Budget wird nach der Entscheidung vom 9. November ausschließlich per Terraform verwaltet.
- Kein Bootstrap, Deployment oder Aufbau von Workshop-Anwendungsressourcen als durchgeführt bestätigt.

Offen: MFA-Status, CDK-/Python-SDK-Zugang mit dem Login-Profil, Python-Umgebung und Bedrock-Inferenzzugriff. Das Budget ist seit dem 9. November angelegt und lesend verifiziert; Terraform-Provider-Zugang funktioniert. Kein zweiter Account nötig.

**Arbeitsstand 9. November 2026:** Der CDK-Budgetentwurf wurde durch Terraform unter `infra/budget/` ersetzt. Der ausdrücklich freigegebene gespeicherte Plan `budget.tfplan` wurde erfolgreich angewendet: **1 angelegt, 0 geändert, 0 gelöscht**. Budget `andre-ai-lab-monthly` in Account `331001679034`: 20 USD monatlich, drei E-Mail-Warnungen bei Überschreiten von 5/10/20 USD, Credits ausgeschlossen. Empfänger nur lokal als sensitive Variable, nicht im öffentlichen Code. CDK bleibt für die Anwendung in Stockholm zuständig; kein Bootstrap oder CloudFormation-Deployment ausgeführt.

**Regionsklärung und Entscheidung:** Andrés echte lesende Registry-Abfrage lieferte `TypeNotFoundException` für `AWS::Budgets::Budget` in Stockholm. Laut veröffentlichten Projekt-SCPs ist CloudFormation in `us-east-1` gesperrt, `budgets:*` aber ausgenommen. Deshalb direkte globale Budgets-API über Terraform. Erfolgreiche Erstellung und anschließende Leseprüfung bestätigen diesen Weg im bestehenden Account; keine manuelle Console-Ausnahme, kein Upgrade und kein Regionswechsel der Anwendung durchgeführt.

**Aktueller Arbeitsstand:** Sortierlogik und getrennte Fehlerfälle sind umgesetzt und auf GitHub nachgewiesen (Etappe 2). Die freigegebenen 35 Dateien wurden als `e7577b1` committet und nach `origin/main` gepusht. Bedrock-Vorschlag vorbereitet: erste Tokenzählung vom Modell nicht unterstützt; danach genau ein separat genehmigter direkter Nova-Lite-Converse-Versuch ohne Tokenzählung durch AWS mit täglichem Tokenlimit abgewiesen (Etappe 3). Noch keine erfolgreiche Inferenz oder Modellantwort. **Supportfall `179423481400635` wurde laut André manuell eingereicht; Bedrock-Inferenz bleibt bis zur Klärung blockiert.** Nächster offener Schritt: Antwort im bestehenden Fall prüfen und effektiven Accountzugang/Quoten klären; keine weiteren Versuche oder parallelen Anträge. Der aktuelle AWS-Fallstatus wurde nicht erneut ausgelesen. Kein Upgrade ausgeführt. Das Budget ist bereits angewendet; der alte Terraform-Plan ist kein offener Plan. Lokalen State vertraulich sichern. Details in `infra/budget/README.md`, `app/README.md` und `experiments/bedrock/README.md`.

**Ergänzender Prüfnachweis 9. November 2026:** Empfänger lokal in ignorierter Datei festgelegt; Terraform-Formatprüfung, Validierung und beide Mock-Tests erfolgreich. Echte lesende Budgets-Abfrage: gleichnamiges Budget nicht vorhanden. Echter Terraform-Plan über Profil `andre-ai-lab` erfolgreich: **1 anlegen, 0 ändern, 0 löschen**. Provider-Login und Accountprüfung funktionieren ohne zusätzlichen Credential-Process. Benachrichtigungen im gespeicherten Plan strukturiert geprüft. Kein Apply; tatsächliche Schreibrechte und Zustellung weiterhin unbestätigt. Nächster Schritt ist die Beurteilung des gespeicherten Plans; Apply bleibt gesondert freizugeben.

**Apply und AWS-Verifikation 9. November 2026 (nach ausdrücklicher Freigabe):** Ausschließlich `terraform apply -input=false -no-color budget.tfplan` ausgeführt; kein neuer Plan und keine Erweiterung des Umfangs. Ergebnis: `Apply complete! Resources: 1 added, 0 changed, 0 destroyed.` Anschließend `DescribeBudget`, `DescribeNotificationsForBudget` sowie für jede der drei Warnungen `DescribeSubscribersForNotification` mit Profil `andre-ai-lab` lesend abgefragt und strukturiert geprüft: `COST`, `MONTHLY`, 20 USD; keine `CostFilters` und keine `FilterExpression` (alle Regionen/Dienste des Accounts); `IncludeCredit=false`. Genau drei `ACTUAL`-/`ABSOLUTE_VALUE`-Warnungen mit `GREATER_THAN` für 5, 10 und 20 USD; jeweils genau ein E-Mail-Empfänger, identisch mit der lokal freigegebenen Adresse, keine SNS-Empfänger. Andere Kostenarten entsprechen den Providerdefaults, einschließlich Steuern und Erstattungen. Budget-Erstellung und zugehörige Lesezugriffe funktionieren; keine Aussage über andere Schreibrechte. Tatsächliche E-Mail-Zustellung noch nicht beobachtet. Budget ist eine verzögerte Kostenwarnung, keine Ausgabensperre; GitHub-Kosten bleiben separat. Lokaler State, Plan und Empfängerdatei bleiben vertraulich und Git-ignoriert. Keine Commits, Pushes oder Veröffentlichung.

## Vollständiger Besucherablauf

1. Ohne Anmeldung zwischen **Anwendung kaputt** und **Pipeline kaputt** wählen.
2. Fehlerkarte auswählen oder den freigegebenen Code/Workflowwert bearbeiten; Änderung als Diff sehen.
3. Backend erstellt einen Lauf mit eigener ID und eigenem Demo-Ausgangsbranch aus einer vertrauenswürdigen Vorlage.
4. Echte GitHub-Actions-Ausführung starten und tatsächlichen Fehler sehen.
5. Agent erstellt genau ein zugeordnetes Ticket mit vorläufiger Diagnose und einen ersten Dokumentationsentwurf.
6. Logs und erlaubte Dateien untersuchen, Patch vorschlagen und echten Reparatur-PR vom Reparaturbranch auf den laufbezogenen Demo-Branch erstellen.
7. Unabhängige geschützte Tests und Änderungsregeln gegen den exakten PR-Stand ausführen.
8. Bei Erfolg automatische Freigabe und Merge; genau den geprüften Artefaktstand pro Lauf veröffentlichen und per Smoke-Test kontrollieren.
9. Reparaturbericht mit belegter Ursache, Änderung, Checks und Deployment ergänzen; Ticket erst nach verifiziertem Abschluss auf erledigt setzen.
10. Bei Misserfolg innerhalb der Grenzen erneut versuchen oder Ticket/PR mit erklärter Übergabe offen lassen. Keine Erfolgsgarantie für beliebigen Besuchercode.

PRs verändern weder Projekt-`main` noch Homepage-Code. Parallele Läufe besitzen getrennte Branches, Artefakte, Tickets und Previews. Wiederholte Events erzeugen keine doppelten Tickets, PRs oder Deployments; aufgeräumte/abgelaufene Läufe sind erkennbar.

## Freigabe und GitHub-Identitäten

Gewählter Entwurf: zwei getrennte GitHub-App-Identitäten. Die **Repair App** erstellt erlaubte Branches/Commits und Reparatur-PRs. Die **Verification App** veröffentlicht den verbindlichen Gesamtcheck aus unabhängiger Verifikation und erteilt nach erfolgreicher Prüfung ein echtes Approval. Beide nur auf den nötigen Repositoryumfang und API-Aktionen beschränken. Der Agent selbst bekommt keine privaten App-Schlüssel; ein vertrauenswürdiger Dienst validiert und vermittelt Schreibaktionen.

Für `demo/<lauf-id>`: PR-Pflicht, mindestens ein gültiges Approval, Pflichtchecks für erlaubte Änderungen/Build/Tests/Artefakte; verbindlichen Gesamtcheck nur von der Verification App akzeptieren. Neue Codeänderungen verwerfen alte Approvals. Kein Force-Push und kein regulärer Bypass für die Apps. Rulesets, App-Reviews und Auto-Merge vor öffentlicher Nutzung an einem Test-PR verifizieren. Geschützte Basisbranches über einen getrennten Provisionierungsschritt erstellen, bevor der Reparatur-PR startet; neue Branch-Erstellung nicht pauschal für Besucher öffnen.

Automatisches Approval und Auto-Merge sind getrennte Schritte. GitHub kann nach erfüllten Pflichtprüfungen automatisch mergen. Für ein echtes sichtbares Approval darf dessen Identität nicht dieselbe wie der PR-Ersteller sein; getrennte Bot-/App-Identitäten, Berechtigungen, GitHub-Plan und Branchregeln vorab praktisch prüfen. Kein gefälschtes Approval oder pauschaler Admin-Bypass.

Der automatische Reviewer bewertet definierte Regeln und unabhängige Prüfergebnisse des aktuellen Commit-SHA. Ein erneuter Commit muss erneut geprüft und gegebenenfalls freigegeben werden. Ein zweites LLM ist keine Voraussetzung und ersetzt keine Tests.

Für menschliche Freigabe dieselben Checks ausführen, anschließend auf einen berechtigten Reviewer warten. Besucher selbst brauchen auch dann keine Rechte. Zunächst automatische Demo-Betriebsart umsetzen; die manuelle Variante als Ausbaupunkt behalten.

## Grenzen und unabhängige Prüfung

Anwendungscode darf nur innerhalb freigegebener Dateien verändert werden. Pipelinepatches dürfen nur freigegebene YAML-Felder ändern. Tests, Sollverhalten, Abhängigkeiten, Secrets, IAM, Workflowberechtigungen und die Steuerung der Reparatur bleiben geschützt. `continue-on-error`, Entfernen von Tests oder Leeren des Artefakts gilt nicht als Reparatur.

Pfade, Größe, Syntax und erlaubte Änderungsfelder deterministisch prüfen. Modellantworten, Logs, Besuchercode und Artefakte als untrusted data behandeln. Keine daraus abgeleiteten freien Shellbefehle ausführen.

Gewählter Sandbox-Entwurf: pro Prüfjob ein frischer VM-basierter GitHub-gehosteter Linux-Runner und darin ein eingeschränkter Docker-Container. Keine Single-CPU-Runner auf gemeinsam genutzter VM und keine dauerhaft mit privaten Zugängen versehenen Self-hosted Runner für fremden Code.

Container ohne Netzwerk, Root-Nutzer, zusätzliche Linux-Capabilities, Docker-Socket oder Hostzugänge betreiben. Schreibgeschütztes Root-Dateisystem und Tests; nur begrenzte Eingabe-/temporäre Ausgabeverzeichnisse. Feste CPU-, Speicher-, Prozess-, Zeit- und Ausgabelimits. Dependencies/Compiler aus vertrauenswürdiger vorbereiteter Umgebung, kein vom Besucher veränderbares Installationsscript. Keine GitHub-, AWS-, Bedrock- oder Atlassian-Credentials im Container. Minimale Runner-Tokenrechte und insbesondere Checkout-Credentials nicht hineinreichen.

Agentenprozess und schreibende Dienste getrennt vom Besuchercode ausführen. Vor Veröffentlichung Endlosschleifen, übermäßigen Speicherverbrauch, Dateizugriffe, Netzwerkversuche, manipulierte Ausgaben und unerlaubte Patches gezielt testen. Container sind eine Schutzschicht, keine absolute Sicherheitsgarantie. Die Akzeptanz dieser Tests und verbleibende Grenzen dokumentieren, bevor der Editor öffentlich wird.

Manipulierter Code läuft in isolierten, zeitlich begrenzten Jobs ohne GitHub-Schreibrechte, Bedrock-Zugang oder Deployment-Credentials. Reine Jobtrennung ist noch kein vollständiges Sandbox-Konzept; Checkout-Tokens, Netzwerkzugang, Cache, Artefakte und Prozessgrenzen prüfen. Fremden Code nicht in privilegierten `pull_request_target`-/`workflow_run`-Kontexten ausführen.

Agent, PR-Erstellung, automatischer Reviewer und Deployment bekommen jeweils begrenzte Rechte. Code- und Testausführung vom berechtigten Lesen/Schreiben in Jira, Confluence, GitHub und AWS trennen. Der schreibende Dienst verarbeitet validierte Daten und führt keine fremden Artefakte aus.

Zunächst maximal zwei Reparaturversuche, feste Zeit-/Tokenlimits und definierte Endzustände. Auch korrekter, bereits reparierter oder nicht reparierbarer Code wird als solcher behandelt. Grüne Tests belegen die geprüften Fälle, keine allgemeine Sicherheit oder Fehlerfreiheit.

## Ablaufzustände und belastbare Ergebniszuordnung

Jeder Lauf besitzt eine serverseitige Zustandsfolge, beispielsweise angenommen → Fehler reproduziert → Diagnose → Patch/PR → Prüfung → Freigabe/Merge → Deployment → Smoke-Test → abgeschlossen. Zusätzlich abgelehnt, fehlgeschlagen, abgebrochen und abgelaufen. Ticket-/Dokumentationsstatus getrennt erfassen. Polling liest diesen Zustand; Browsermeldungen entscheiden weder über Erfolg noch über Berechtigungen.

Pro Phase erwartete Eingaben, Timeout, Wiederholung und zuständigen Dienst festlegen. GitHub-Events dürfen doppelt, verspätet oder in anderer Reihenfolge eintreffen. Webhooks vor Verarbeitung per Signatur prüfen und anhand Delivery-ID deduplizieren; Repository, Run-ID, Workflow und Commit-Zuordnung kontrollieren. Ein verspäteter Erfolg darf einen abgebrochenen Lauf nicht veröffentlichen. Ein Abbruch beendet weitere Modellaufrufe und Deployments; Cleanup auch nach Abstürzen periodisch nachholen.

Prüfnachweis bindet Ausgangscommit, PR-Head, vertrauenswürdige Prüfversion, unveränderliche Artefakt-ID und Inhaltsdigest zusammen. Vor Merge/Deployment Zuordnung erneut prüfen. Merge-/Squash-Commit kann eine andere SHA als der geprüfte PR-Head haben: Übereinstimmung des relevanten Quellstands nachweisen oder den Merge-Stand neu prüfen. Nach erfolgreicher Prüfung keine veränderlichen Artefakte gleichen Namens neu bauen oder austauschen. Containerimages per Digest und Abhängigkeiten über Lockdateien festlegen; Actions-Versionen ebenfalls unveränderlich referenzieren.

Ein kryptographischer Digest belegt die Zuordnung, nicht die Sicherheit des Inhalts. Archive, Pfade, Symlinks, Dateitypen und Größen vor Übernahme kontrollieren; fremde Artefakte weder im privilegierten Dienst ausführen noch außerhalb des Zielverzeichnisses entpacken. Gemeinsame beschreibbare Caches zwischen fremden Läufen und privilegierter Steuerung vermeiden.

## Kriterien vor öffentlicher Freigabe

- **Funktion:** Beide Modi vom Fehler bis zum nachweisbaren Ergebnis durchlaufen; auch bereits korrekter und nicht reparierbarer Code sowie Ausfälle von Modell, GitHub und Atlassian werden ehrlich dargestellt. Dieselben versionierten Evaluationsfälle nach wesentlichen Änderungen erneut ausführen.
- **Zugriff:** Anonyme Besucher bekommen nur begrenzte Laufrechte. Nicht erratbare Laufkennungen ersetzen keine Berechtigung für Start, Abbruch oder Änderungen. Session-/Laufbindung, serverseitige Eingabeprüfung, Größenlimits und Schutz vor unerwünschten browserübergreifenden Aktionen festlegen; CORS allein ist kein Missbrauchsschutz.
- **Darstellung:** Code, Logs, Modelltexte und Ticketinhalte als Daten rendern; HTML/Markdown und Links entsprechend absichern. Keine Skripte aus Logs oder Berichten ausführen. Besucher-Simulation bevorzugt als validierte Routingergebnisse in vertrauenswürdiger Darstellung zeigen. Falls aktiver Besuchercode als Preview veröffentlicht wird, eigene Origin, restriktive Einbettung und keine geteilten Cookies/Tokens verwenden.
- **Grenzen:** Serverseitiges globales Kontingent atomar vor kostenpflichtiger Arbeit reservieren, anfangs höchstens ein aktiver öffentlicher Lauf. Zusätzliche Session-/IP-Grenzen, kurze Laufzeiten und höchstens zwei Reparaturversuche; bei Bedarf Bot-Challenge. Ein Cookie pro Besucher verhindert keine automatisierten Mehrfachstarts. Start-Endpunkt muss abschaltbar sein; Quoten begrenzen auch Wiederholungen, Branches, Jira-Tickets und Confluence-Seiten. Bereits entstandene und verzögert abgerechnete Kosten bleiben möglich.
- **Betrieb:** Verwaiste Jobs, Branches, Previews und temporäre Dateien mit überprüfbarer TTL bereinigen. Öffentliche PRs und deren Git-Historie sind nicht durch Branch-Löschen verlässlich entfernt; Aufbewahrung von Referenzbelegen und Löschmöglichkeiten für versehentlich eingereichte Daten gesondert festlegen. Secrets sicher speichern, Rotation und Wiederherstellung des Betriebs einmal erklären.
- **Besuchererlebnis:** Wartezeit und Warteschlange anzeigen; verständlicher Fehler-/Abbruchzustand; klare Kennzeichnung aufgezeichneter Abläufe. Tastaturbedienung, mobile Ansicht und reduzierte Animation berücksichtigen. Sichtbarer Code-Diff, belegte Prüfergebnisse und Architektur erklären den Mehrwert.

Diese Kriterien schrittweise mitbauen. Sie sind Bedingungen für den öffentlichen Editor, nicht Voraussetzungen für Andrés erste lokale Lernübung. Personenbezogene Eingaben vermeiden; Übertragung an Modellanbieter, öffentliche GitHub-Inhalte und Aufbewahrung auf der Demo verständlich erläutern.

## Architekturentwurf

```text
Website: Sortieranlage + Editor + Pipeline + Kanban + Reparaturbericht
  → Backend mit Laufkontingent und serverseitiger GitHub-Anbindung
  → GitHub Actions: Build / Tests / Artefaktprüfung scheitern
  → Agent (Python) → Amazon Bedrock
      → Ticket / Dokumentationsentwurf über begrenzte Werkzeuge
      → Reparaturbranch + echter PR
  → unabhängige Verifikation des PR-Commits
  → automatische Freigabe + Merge in Demo-Branch des Laufs
  → geprüfte Artefakte → isolierte Demo-Preview → Smoke-Test
  → Jira aktualisieren + Confluence-Bericht abschließen
  → tatsächliche Ereignisse / Ergebnisse an Website zurückgeben

Anwendungsinfrastruktur: TypeScript/CDK und CloudFormation in Stockholm
Globales Budget: Terraform → Budgets-API in us-east-1; separater State
AWS-Zugang von GitHub: OIDC, nach Prüfung des Accountmodells
Kostenüberwachung: eigener Stack; AWS und GitHub separat messen
```

Website zeigt tatsächliche Ereignisse und Werkzeugergebnisse, keine internen Gedanken des Modells. Animierte Architekturkomponenten folgen echten Aktivitäten. Statuslatenzen und Runner-Wartezeit sichtbar machen; kein sofortiges Feedback versprechen. GitHub Actions orchestriert; kein CodeBuild, Step Functions oder CodePipeline im Grundpfad.

Jira und Confluence bleiben zunächst privat. Eine eigene kleine Website-Ansicht zeigt ausgewählte Daten des jeweiligen Laufs über das Backend. Kein vollständiger Jira-Nachbau. Reale API-IDs und Ergebnislinks korrekt zuordnen; lokale Adapter dürfen bis zur echten Integration nicht als Atlassian-Integration ausgegeben werden.

## Etappe 1 – Kostenüberwachung mit Terraform und CDK-Einordnung

Codex prüft das vorhandene Grundgerüst und ordnet Einstiegspunkt, Stack und erzeugte CloudFormation-Vorlage kurz ein. Kein eigener Grundlagenblock zu TypeScript oder manuelles Nachbauen des Scaffolds. Budgetkonfiguration unter `infra/budget/` per Terraform generieren und prüfen lassen; die CDK-App bleibt ein Anwendungsplatzhalter. Unterschiede zwischen globaler API und regionalem CloudFormation-Stack kurz am konkreten Fall erklären.

`.gitignore` vor weiteren Artefakten prüfen: `node_modules/`, `cdk.out/`, `.venv/`, Python-Caches, `.env`, lokale Konfiguration und Laufartefakte ausschließen. Code, feste Testfälle, Paket-Lockdateien und geeignete CDK-Kontextwerte versionieren. Credentials bleiben außerhalb des Repositorys. Empfängeradressen nicht unnötig im öffentlichen Code hinterlegen; sie können trotzdem in Vorlagen und CloudFormation sichtbar sein.

Separaten Terraform-Budgetzustand definieren: 20 USD monatlich, Warnungen bei 5, 10 und 20 USD. Credits bei der Kostenmessung nicht abziehen. `fmt`, `validate` und Mock-Tests lokal ausführen; Lockdatei versionieren, State/Plan und echte Empfängerdateien ignorieren. Ein echter Plan benötigt AWS-Zugriff und passende Credentials; Ergebnis gemeinsam kontrollieren, Apply erst nach konkreter Freigabe. Anschließend Budget und Benachrichtigungen lesend verifizieren. Budget nicht zugleich per CDK anlegen.

Das Terraform-Budget benötigt keinen CDK-Bootstrap. Falls später für die Anwendung Bootstrap erforderlich ist, Ressourcen und IAM-Rollen vorher erklären und die Konfiguration per IaC prüfen. Ein bewusst ausgeführtes `cdk bootstrap` bleibt ein IaC-Bereitstellungsschritt. Keine stillen manuellen Ersatzlösungen.

Erfolg: André versteht Budgetverhalten und Grenzen, erkennt das einzelne Budget und seine Warnungen im Terraform-Plan und weiß, was das Deployment anlegt. Keine zeilenweise Erklärung des generierten Codes erforderlich.

## Etappe 2 – Sortierlogik und GitHub-Pipeline ohne KI

Kleine TypeScript-Routingfunktion mit klaren Anforderungen, drei Stationen, festen Paketen und unabhängigen Tests bauen. Zunächst Ergebnisse als Daten ausgeben; die aufwendige Animation folgt später.

**Lokaler Nachweis 9. November 2026:** `app/src/routing.ts` ordnet Berlin → `berlin`, Hamburg → `hamburg`, München → `munich` zu. Sechs feste Demopakete werden als JSON ausgegeben. Sechs fachliche Testfälle mit separaten Paket-IDs und expliziten Sollstationen bestehen (`npm test`, Exitcode 0). Die Sollwerte stammen weder aus der Routingimplementierung noch aus den Demodaten. Unter `app/scenarios/berlin-to-hamburg/` liegt die getrennte Fehlervariante: Berlin wird absichtlich nach `hamburg` geschickt. Derselbe unveränderte Testvertrag meldet dort zwei fehlgeschlagene Berliner Fälle und vier erfolgreiche Fälle für Hamburg/München (`npm run test:scenario`, Exitcode 1). Die TypeScript-Typprüfung besteht auch für den fachlich falschen Code: Typkorrektheit beweist kein korrektes Routing. Der funktionierende Ausgangsstand bleibt erhalten. Befehle und Grenzen in `app/README.md`. Alle Prüfungen lokal; keine Animation, KI-Anbindung, AWS-/Cloudzugriffe, GitHub-Aktionen, Commits oder Pushes in diesem Arbeitsschritt. Noch keine Isolation gegen manipulativen Fremdcode.

Vertrauenswürdigen GitHub-Actions-Workflow für Build, Tests, Artefaktprüfung und Ergebnisartefakte erstellen. Korrekte Referenz ausführen. Danach falsches Routing und getrennt davon falschen Artefaktpfad reproduzieren. Das Fehlen erforderlicher Dateien explizit als Fehler prüfen.

**Vorbereitung und lokaler Nachweis 9. November 2026:** App-eigene `package-lock.json` mit TypeScript 7.0.2, `npm ci --ignore-scripts --no-audit --no-fund`, Typprüfung und Build nach `app/dist/` ergänzt. `.github/workflows/app-ci.yml` prüft wahlweise Referenz oder getrennten Routingfehler; `.github/workflows/app-pipeline-error.yml` verwendet die korrekte Anwendung und absichtlich `app/build` als gemeinsamen Prüf-/Uploadpfad. Ausschließlich `workflow_dispatch`, nur `contents: read`, Checkout ohne persistierte Credentials, Actions per Commit-SHA, kein AWS-/OIDC-Zugang oder Projekt-Secret, kein Deployment. Artefaktprüfung verlangt drei nichtleere JS-Dateien und schlägt bei fehlendem Pfad fehl; Upload setzt zusätzlich `if-no-files-found: error`. Referenz lokal grün (6/6 Tests, Build und kompilierte Demo); Routingfehler separat rot (2 Berliner Fälle); Pipelinefehler nach erfolgreichem Build/Test mit Exitcode 1 wegen fehlendem `app/build`. Leere und unvollständige Artefaktordner ebenfalls abgewiesen. Beide YAML-Workflows mit actionlint 1.7.7 erfolgreich geprüft. GitHub-Runner und echter Upload noch nicht erprobt; keine Workflowstarts, AWS-Zugriffe, Commits oder Pushes. Noch keine unabhängige privilegierte Reparatursteuerung oder Fremdcode-Sandbox.

Logs, Status, Lauf-ID und Quelldateien strukturiert erfassen. Beide Fehler ohne KI erklären können. Zunächst Fehlerkarten, später im öffentlichen Ziel zusätzlich begrenzter Editor.

**GitHub-Nachweis 9. November 2026 (jeweils ausdrücklich freigegeben):** Commit `e7577b1ed8f7f59fe7013a6e1c08e3b606aa486c` im öffentlichen Repository `andre-fricke/aws-ai-workshop`. Genau drei manuelle Läufe: [Referenz erfolgreich](https://github.com/andre-fricke/aws-ai-workshop/actions/runs/42624681867), einschließlich Upload von `parcel-sorter-42624681867-1`; danach [Routingfehler](https://github.com/andre-fricke/aws-ai-workshop/actions/runs/42625481766), Berliner Tests mit `actual: 'hamburg'`, `expected: 'berlin'`, Exitcode 1; anschließend [Pipelinefehler](https://github.com/andre-fricke/aws-ai-workshop/actions/runs/42625772110), erfolgreiche Typprüfung/Tests/Build, aber `ENOENT` für `app/build`, Exitcode 1. Beide Fehlerläufe auf demselben Commit, Upload jeweils übersprungen und per API jeweils null Artefakte bestätigt. Keine Reparaturen oder weiteren Läufe gestartet.

## Etappe 3 – Bedrock verstehen und Reparaturvorschläge erzeugen

**Manuelle Einreichung bestätigt, 9. November 2026:** André meldet Supportfall **`179423481400635`** als manuell eingereicht. Dies ersetzt den früheren lokalen Nichtversandstatus für den Gesamtvorgang; der vorherige API-Zugriff blieb erfolglos. Keine erneute Erstellung oder zusätzliche Quotenanfrage durch Codex. Bedrock-Inferenz bleibt bis zur Klärung des Accountzugangs und der effektiven Quoten blockiert. Nächster Schritt: AWS-Antwort im bestehenden Fall prüfen; konkrete neue Modellaufrufe benötigen danach eine neue Freigabe. Keine erfolgreiche Inferenz oder Reparatur behauptet. AWS-Fallstatus und Supportantwort nicht neu abgefragt. Request-/Response-/Fehlerdateien, `.venv/`, Terraform-State/-Plan und lokale Budgetempfängerdatei bleiben Git-ignoriert und von der Veröffentlichung ausgeschlossen.

**Support-API-Prüfung nach bedingter Versandfreigabe, 9. November 2026:** Genau eine lesende `DescribeCases`-Abfrage mit dem bestehenden Profil scheiterte am offiziellen Support-Endpunkt in `us-east-1` mit HTTP 400, `SubscriptionRequiredException`: `Amazon Web Services Premium Support Subscription is required to use this service.` Request-ID `f8a768d7-4f95-40a4-a6b5-5233d1b60acc`, keine Retries. Damit keine Duplikatprüfung möglich und kein `CreateCase` ausgeführt. **Case-ID: keine; lokaler Versandstatus NOT_SUBMITTED_API_UNAVAILABLE**, kein AWS-Case-Status vorhanden. Kein Fall versendet oder Upgrade/Quotenantrag ausgelöst. Offizieller Ersatzweg: AWS Settings → Support, zuerst bestehende gleichartige Fälle prüfen; nur ohne Duplikat Project support → Create case und den unveränderten freigegebenen Text einmal einreichen. Bei unklarem Ergebnis Fallliste kontrollieren statt erneut senden. Details in `experiments/bedrock/quota-request-draft.md`; maschinenlesbarer lokaler Nachweis in ignorierter `runs/bedrock-routing/support-api-check.json`.

**Einheitlicher Supportentwurf 9. November 2026 (noch nicht gesendet):** Nach Prüfung der offiziellen Supportdokumentation für das neue AWS-Erlebnis wurde `experiments/bedrock/quota-request-draft.md` auf genau einen Accountklärungsfall zugeschnitten. Vorgesehener Eingang: AWS Settings → Support → Project support → Create case, Basic Support; Bitte um interne Weiterleitung an Bedrock statt parallelem Quotenfall. Ausdrückliche Frage nach zusätzlicher Accountaktivierung/Verifizierung; gewünschte direkte Nova-Lite-Quote in Stockholm 10.000 TPM, 2 RPM und falls nötig 100.000 modellbezogene Tokens/Tag. Cross-Model-Tageslimit 150.000.000 unverändert. Der frühere Cross-Region-Einstiegsantrag ist damit als aktueller Entwurf ersetzt; keine Cross-Region-Quota-Erhöhung beantragt. Vollständiger englischer Text und konkrete UI-Schritte lokal vorbereitet. AWS muss Zuständigkeit und mögliche Freischaltung im bestehenden Free plan bestätigen; regulärer Technical Support unter Basic Support nicht zugesichert. Kein Formular befüllt, kein Fall angelegt/gesendet, keine neuen AWS-Accountabfragen oder Inferenzversuche, Quotenanträge, Upgrades, Abos oder Reservierungen in dieser Vorbereitung.

**Präzisierte Quotenprüfung und vorbereiteter Antrag, 9. November 2026:** Tatsächlich angewendete Werte in Stockholm einzeln mit `GetServiceQuota` bestätigt: Nova Lite On-Demand-TPM `L-70423BF8` = 0, RPM `L-E386A278` = 0; jeweils `Adjustable=false`. Das zusätzlich angezeigte modellbezogene Tageslimit `L-45E0AD92` = 0, ebenfalls false. **Cross-Model Max Tokens Per Day `L-E3F10727` = 150.000.000, nicht 0**, false, accountweit über Modelle innerhalb der Region (kein Restkontingent). Alle gelesenen Quoten sind accountbezogen und nicht global; das macht modellbezogene Quoten nicht modellübergreifend. Cross-Region-TPM für Nova Lite `L-7C42E72A` = 0, `Adjustable=true`: laut AWS administrativer Einstieg für kombinierte TPM-/Tageslimit-Anträge. Entwurf unter `experiments/bedrock/quota-request-draft.md`: Einstieg Cross-Region-TPM 10.000 transparent benannt, eigentliches Betriebsziel direkte On-Demand-TPM 10.000 und RPM 2; gegebenenfalls modellbezogen 100.000 Tokens/Tag, falls nach TPM-Erhöhung weiter erzwungen. Cross-Model-Tageswert unverändert lassen. Begründung und Frage zur effektiven Tageslimitdurchsetzung vorbereitet. Kein Antrag abgesendet, kein Supportfall erstellt, keine Quotenänderung oder Inferenz in dieser Prüfung, kein Modellwechsel/Upgrade.

**Vorbereitung und lesender Nachweis 9. November 2026:** `experiments/bedrock/` enthält Python-Aufruf, fachlichen Kontext, kuratierten Auszug aus den tatsächlichen Routingfehlerlogs, lokale Struktur-/Änderungsvalidierung und zehn erfolgreiche Offline-Tests. Boto3 1.43.126 mit CRT in ignorierter `.venv/` installiert, exakte Abhängigkeiten festgehalten. SDK-Identitäts-/Modell-/Quoten-Lesezugriffe mit `andre-ai-lab` erfolgreich. Nova Micro/Lite melden `AUTHORIZED` und Agreement/Entitlement/Region `AVAILABLE`; Micro benötigt in Stockholm ein EU-Inferenzprofil (mögliche Ziele Frankfurt, Stockholm, Irland, Paris), Lite bietet zusätzlich direkte On-Demand-Inferenz. Vorläufige Empfehlung für den kleinen Reparaturversuch: `amazon.nova-lite-v1:0` direkt in `eu-north-1`, ohne Cross-Region-Fallback. Relevante Lite-Inferenzquoten für RPM, TPM und tägliche Tokens melden jedoch jeweils 0; auch gelesene Micro-/Nova-2-Lite-Inferenzquoten 0. Zugang deshalb noch nicht als tatsächlich inferenzfähig nachgewiesen; keine Quotenänderung beantragt.

**Geplanter einzelner Aufruf, noch nicht freigegeben/ausgeführt:** Request offline vorbereitet (2.903 UTF-8-Bytes); lokales Limit 12.000 Bytes, maximal 4.096 Eingabetokens nach kostenloser Tokenzählung, `maxTokens=512`, Temperatur 0, keine Werkzeuge, kein Streaming, keine Retries oder Ersatzmodelle. AWS Price List für Nova Lite On-Demand in Stockholm gelesen: 0,000065 USD/1.000 Eingabetokens, 0,00026 USD/1.000 Ausgabetokens, höchstens 0,00039936 USD vor Steuern innerhalb der Versuchsgrenzen (Preisstand 1. November 2026). Native Structured Outputs werden für Lite nicht unterstützt; JSON wird angefordert und lokal streng geprüft, ohne Patchanwendung oder Ausführung. Fehlerhafte/abgebrochene Antworten lösen keinen weiteren Aufruf aus. Nullquoten vor Inferenz klären; der Runner bricht bei gemeldeter Nullquote ab. `CountTokens` und `Converse` bislang nicht aufgerufen. Inferenz erst nach ausdrücklicher Freigabe; Details, Modellgrenzen und Quellen in `experiments/bedrock/README.md`.

**Tatsächlicher Versuch nach Freigabe 9. November 2026:** Freigegeben waren zuerst die Tokenzählung und danach genau ein Nova-Lite-Inferenzversuch direkt in Stockholm, ausschließlich bei höchstens 4.096 gezählten Eingabetokens, maximal 512 Ausgabetokens, erwartete Inferenzkosten unter 0,001 USD. Der unveränderte Request wurde über Boto3/CRT mit dem bestehenden Profil verwendet; STS bestätigte den erwarteten Account. Bedrock-Runtime-Endpunkt `https://bedrock-runtime.eu-north-1.amazonaws.com`; `total_max_attempts=1` (keine SDK-Retries). Genau eine `CountTokens`-Anfrage für `amazon.nova-lite-v1:0` scheiterte mit HTTP 400, `ValidationException`: `The provided model doesn't support counting tokens.` Request-ID `717235ba-3290-4c8e-8181-ebce75b24560`, `RetryAttempts=0`. Die Eingabetokengrenze war damit nicht nachgewiesen: **kein Converse-/Inferenzaufruf**, keine Modellantwort, kein validierter Reparaturvorschlag, keine Code-Reparatur und keine Inferenzkosten. Keine Wiederholung, Quotenänderung, Upgrades oder Modell-/Regionsfallbacks. Der vorbereitete Tokenzählungsweg ist für Nova Lite nicht nutzbar und muss vor einer weiteren Freigabe neu geklärt werden; die Bytezahl ist kein Ersatznachweis. Lokale Git-ignorierte Nachweise in `runs/bedrock-routing/`, technische Details in `experiments/bedrock/README.md`.

Python-Umgebung anlegen und aktuelle SDK-Abhängigkeiten festhalten. Den Identitätszugang separat prüfen; CLI-Erfolg allein beweist keine SDK-Kompatibilität. Falls nötig den offiziell dokumentierten `credential_process`-Weg verwenden.

**Einzelner Converse-Versuch nach neuer ausdrücklicher Freigabe, 9. November 2026:** Nutzer entfernte die Bedingung von 4.096 gezählten Eingabetokens ausdrücklich und genehmigte genau den unveränderten Request mit maximal 12.000 UTF-8-Bytes, maximal 512 Ausgabetokens, ohne CountTokens oder SDK-Retries. Vergleich mit vorbereitetem Kontext und dem zuvor dokumentierten Request-Hash bestätigt: unverändert. Gespeicherte JSON-Datei 3.008 Bytes, kompakte Darstellung 2.903 Bytes, tatsächlich gesendeter HTTP-Body 2.938 Bytes. Genau ein `Converse` für `amazon.nova-lite-v1:0` direkt an `bedrock-runtime.eu-north-1.amazonaws.com`, Temperatur 0, `maxTokens=512`, `total_max_attempts=1`; ein tatsächlicher HTTP-Sendeversuch und `RetryAttempts=0` bestätigt. AWS antwortete HTTP 429, `ThrottlingException`: `Too many tokens per day, please wait before trying again.` Request-ID `ebd73222-fedd-4d96-941a-3f821a3b3f1e`. Keine Modellantwort und keine Tokenverbrauchszähler zurückgegeben; deshalb keine tatsächlichen Tokenkosten berechenbar. Keine Vorschlagsvalidierung möglich, keine Reparaturanwendung, Quotenänderungen, Upgrades oder Fallbacks. Kein weiterer Aufruf; Freigabe für den einzelnen Versuch verbraucht. Lokale Nachweise `runs/bedrock-routing/attempt.json` und `inference-error.json` bleiben Git-ignoriert.

Verfügbares Textmodell und tatsächlichen Zugriff in Stockholm prüfen. Katalogeintrag und Inferenzberechtigung unterscheiden. Vor dem ersten Aufruf Preis, Ausgabegrenze und gegebenenfalls beteiligte Regionen eines Inference Profiles erklären.

Zunächst genau einen Aufruf mit Fehlerlog und erlaubter Datei durchführen. Antwort als strukturierten Änderungsvorschlag validieren. Noch nichts automatisch anwenden. Prompt, Modellkennung, Laufzeit und Tokenverbrauch festhalten.

Erfolg: André kann erklären, welcher Kontext an das Modell ging und warum der Vorschlag noch überprüft werden muss.

## Etappe 4 – Kontrollierte Agentenschleife

Agent im GitHub-Actions-Ablauf einbinden. Zunächst gezielte Werkzeuge für Logs, erlaubte Dateien und Patchvorschläge; die Rechte der späteren schreibenden Werkzeuge separat begrenzen. Tool-Schema, Argumentprüfung, Ausführung und Endzustände verstehen.

Anwendungs- und Pipelinefehler unterscheiden. Vor dem Pipelinepatch erlaubte Workflowfelder festlegen und unabhängige Kontrollen außerhalb dieser Datei halten. Kein genereller Schreibzugriff auf Workflows.

Erst einen vorgeschlagenen Patch prüfen und isoliert testen, dann die begrenzte Schleife automatisieren. Maximal zwei Versuche, feste Limits, klare Übergabe. Agentenstart und Fehlerbehandlung nicht vom bearbeitbaren Demo-Workflow abhängig machen; auch dessen Fehlschlag muss beobachtbar bleiben.

Erfolg: André kann eine Ursache aus der richtigen Schicht bestimmen und erklären, welche Regeln unabhängig vom LLM erzwungen werden.

## Etappe 5 – Qualität und unerlaubte Reparaturen prüfen

Einen kleinen versionierten Evaluationssatz aufbauen: reparierbare Fehler, bereits korrekter Code, unzureichender Kontext, nicht erlaubte Änderungen und ein nicht innerhalb der Grenzen reparierbarer Fehler. Manipulative Anweisungen in Logs als untrusted data behandeln.

Prüfen, ob Tests unverändert bleiben und eine bloße feste Beispielantwort durch zusätzliche geschützte Testfälle auffällt. Erfolg nur bei erlaubtem Patch und bestandener Verifikation zählen. Testfälle außerhalb des Agentenkontexts halten.

Reparaturquote, unerlaubte Änderungen, Versuche, Laufzeit und Tokenverbrauch erfassen. Bei kleinem Testsatz Ergebnisse nicht als allgemeine Zuverlässigkeitsgarantie darstellen. Code-, Prompt- und Modellversion festhalten. Nach Änderungen denselben Satz erneut ausführen.

Erfolg: André kann eine Verbesserung anhand der Ergebnisse belegen und deren Grenzen benennen.

## Etappe 6 – Echte PRs, Freigabe und Demo-Deployment

Serverseitige GitHub-Integration sowie Branches pro Lauf aufbauen. Reparatur-PR gegen den Demo-Ausgangsbranch erstellen; Projekt-`main` bleibt unverändert. Erforderliche Events und Tokens prüfen: nicht voraussetzen, dass vom `GITHUB_TOKEN` erzeugte Änderungen alle Folgeworkflows automatisch starten.

Pflichtprüfungen an exakten Commit binden. Getrennte Identität für sichtbares automatisches Approval prüfen und anschließend Auto-Merge aktivieren. Noch kein öffentlicher Zugriff. Den manuellen Freigabemodus als definierte Alternative dokumentieren.

AWS-Berechtigungen über OIDC und CDK vorbereiten, sofern im bestehenden Account unterstützt. Deploymentdienst übernimmt ausschließlich unabhängig geprüfte Artefakte des zugehörigen Laufs. Keine generierten CDK-/CloudFormation-Änderungen automatisch ausführen. Vorschau-Hosting, Origin-Isolation, Smoke-Test, letzte funktionierende Version und Bereinigung vor Veröffentlichung festlegen.

Erfolg: Echte Pipeline scheitert, echter Reparatur-PR wird geprüft, automatisch freigegeben/zusammengeführt und genau das geprüfte Ergebnis kontrolliert bereitgestellt.

## Etappe 6b – Ticket und Dokumentation integrieren

Zuerst strukturierte Schnittstellen und lokale Adapter für Ticket, Statusübergang und Reparaturbericht erstellen. Anschließend Jira Cloud und Confluence Cloud anbinden. Free-Pläne, API-Berechtigungen, Authentifizierung und Limits prüfen; persönliche Accountregistrierung nur gemeinsam. Keine Besucher zu Atlassian einladen.

Ticket enthält Fehlerklasse, Laufbezug, beobachteten Fehler, erwartetes Verhalten und Links zu PR/Checks. Statusfolge zunächst Offen → Analyse → Reparatur → Prüfung → Erledigt; erfolglose Läufe bleiben mit Übergabe offen.

Confluence-Bericht wächst vom vorläufigen Befund zum Abschluss mit Ursache, Patch, Testnachweisen und Deployment. Hypothesen und bestätigte Befunde unterscheiden. API-Wiederholungen müssen vorhandene Einträge aktualisieren statt Duplikate erzeugen. Scheitert eine externe Integration, Code-Reparaturerfolg und Dokumentationsstatus getrennt anzeigen.

Erfolg: Ein Lauf besitzt tatsächlich zugeordnete Jira- und Confluence-Einträge; Website kann ausgewählte Informationen später ohne Atlassian-Anmeldung darstellen.

## Etappe 7 – RAG als gezielte Vertiefung (für erste Demo nicht blockierend)

Projektregeln und kurze Reparaturanleitungen ergänzen. Erst den Unterschied zwischen vollständig mitgegebenem Kontext und gezieltem Retrieval verstehen. Anschließend Chunking, Embeddings, Vektorsuche und Quellenmetadaten an einem kleinen lokalen Index umsetzen.

Embedding-Modell, Dimension und Dokumentversion festhalten. Frage und Dokumente mit kompatiblem Verfahren einbetten. An Fällen mit relevantem und irrelevantem Zusatzwissen messen, ob Retrieval die Reparaturen verbessert. RAG nicht als Voraussetzung für die erste Reparatur oder als garantierte Verbesserung darstellen.

Optional verwaltete Bedrock Knowledge Bases vergleichen, sofern Dienste, Region und Kosten passen. MCP oder ein Agentenframework erst später einordnen, nachdem die einfache Werkzeugschleife verstanden wurde.

Erfolg: André kann begründen, wann RAG hilfreich ist, und Retrievalfehler von Modell- oder Ausführungsfehlern unterscheiden.

## Etappe 8 – Betrieb und Kosten verstehen

Korrelations-/Lauf-ID, Phasenzustände, Modell-/Promptversion, Fehlerstatus, Laufzeit und Tokenverbrauch erfassen. Keine Credentials oder vollständigen privaten Inhalte protokollieren. Relevante CloudWatch-Metriken und Alarmierung ergänzen.

Gezielt Modellzugriffsfehler, Runner-Timeout und einen abgebrochenen Lauf untersuchen. Wiederholungen dürfen keinen unkontrollierten zweiten Deploymentlauf auslösen. Parallele Läufe und deren Arbeitsbereiche unterscheiden können.

Kosten pro Beispielausführung aus tatsächlicher Nutzung abschätzen. Budgetmeldungen haben Verzögerungen und sind keine Ausgabensperre. Infrastrukturkosten der Pipeline und Bereitstellung zusätzlich zur Modellinferenz berücksichtigen.

## Etappe 9 – Website-Demo und Architekturansicht

TypeScript-Oberfläche für beide Modi erstellen: animierte Sortieranlage, vorbereitete Fehlerkarten und begrenzter Editor, Pipeline, Logs, Besucher-/Reparatur-Diffs, echter PR, Prüf-/Freigabestatus, Kanban und Dokumentation. Zunächst privat testen.

Drei Stationen und tatsächliche Routingergebnisse darstellen. Im Pipelinefehlerfall letzte funktionierende Version und ausstehendes Deployment unterscheiden. Vorher-/Nachher-Ergebnis pro Lauf anzeigen. Anonyme Besucher starten über das Backend; niemals direkt mit einem GitHub-Token.

Entschieden: **Polling** für den Einstieg. Der Browser fragt das Backend beispielsweise alle drei Sekunden nach dem Laufzustand; nach Endzustand stoppen, bei unsichtbarer Seite/Fehlern verlangsamen. Die Animation läuft davon unabhängig lokal flüssig. Streaming meint späteren Ereignispush per SSE oder WebSockets vom Backend zum Browser, nicht Kafka. Kafka ist für diese Demo nicht vorgesehen. Architekturansicht und Erklärung ergänzen, aktive Komponenten anhand realer Ereignisse hervorheben. Bei fehlgeschlagener Reparatur keine erfolgreiche Animation abspielen.

Vor öffentlichem Betrieb Nutzung und Kosten messen: globales Kontingent, begrenzte Parallelität, Sessions, Timeouts, maximale Versuche, TTL für Branches/Previews/Artefakte und abschaltbarer Start-Endpunkt. Anonymes Starten erfordert Missbrauchsbegrenzung. Keine feste 50-USD-Garantie aus Rate Limits oder Budgetwarnungen ableiten.

Danach Homepage-Technik prüfen. Separate Subdomain und Fallstudie bevorzugt, iframe optional. Hosting/DNS über IaC soweit unterstützt. Bedienelemente, responsive Darstellung und Zugriff ohne Anmeldung prüfen. Keine Veröffentlichung allein aufgrund dieses Plans voraussetzen.

## Etappe 10 – Eigenständig steuern, verstehen und abschließen

André beschreibt ein neues Fehlerszenario und dessen Erfolgskriterien, lässt Umsetzung und Tests durch Codex erzeugen und beurteilt das tatsächliche Ergebnis. Danach mit KI-Unterstützung einen absichtlich eingebauten Fehler der Ablaufsteuerung eingrenzen. Entscheidend ist, dass André passende Prüfungen veranlasst und Ursache sowie Wirkung erklären kann; Arbeit ohne KI oder manuelles Coding wird nicht verlangt. Offene Verständnisfragen dokumentieren.

Fallstudie erstellen: Problem, Architektur, Entscheidungen, Demoablauf, Evaluationsergebnisse, Kosten und Grenzen. Gegebenenfalls einen ausdrücklich gekennzeichneten aufgezeichneten Lauf bereitstellen.

Entscheiden, welche Demo-Ressourcen weiterlaufen sollen. Nicht benötigte Ressourcen über CDK zurückbauen, Budget und Kostenüberwachung separat erhalten. Retain-Einstellungen, S3-Objekte, Artefakte, Logs, Runner und Bootstrap-Ressourcen prüfen. Später aktualisierte Abrechnung kontrollieren.

## Kostenrahmen und Accountgrenzen

Kein dauerhaft laufender EKS-Cluster für die öffentliche Demo. Eine optionale Kubernetes-Variante bleibt im Ausbauplan; sie ist keine Voraussetzung für den KI-Nachweis.

Ziel: etwa **20 USD monatlich** bei geringer öffentlicher Nutzung. Andrés maximale monatliche Zahlungsbereitschaft: **50 USD insgesamt**. Nicht als vorhandenen technischen Kostendeckel darstellen. Keine zusätzlichen kostenpflichtigen Abos ohne vorherige Abstimmung.

Vor Implementierung kalkulieren, vor Veröffentlichung messen: Modell-/Tokenkosten, GitHub-Runner, Cache-/Artefaktspeicher, API, Hosting, Logs, Ergebnisdaten und gegebenenfalls Atlassian. Öffentliche Standard-GitHub-Runner können kostengünstig sein; konkreten GitHub-Plan, Sichtbarkeit, Nutzungsbedingungen und Speichergrenzen prüfen. Öffentliches Repository ist als Ziel entschieden; tatsächlichen Zustand lesend prüfen und Veröffentlichung bewusst durchführen. Öffentliche Eingaben und Ergebnisse im Produkt klar kennzeichnen.

Jira-/Confluence-Free-Pläne bevorzugt; Limits und API-Nutzbarkeit praktisch bestätigen. Keine eingebauten kostenpflichtigen KI-/Automatisierungsprodukte erforderlich voraussetzen. Guthaben nicht mit dauerhaft kostenlosem Betrieb verwechseln.

Live-Laufzahl aus gemessenen Kosten ableiten. Bei ausgeschöpftem Kontingent keinen weiteren Lauf annehmen; stattdessen klar markierten aufgezeichneten Beispieldurchlauf anbieten. Ein anfängliches internes Budget von 20 USD mit Warnungen bei 5/10/20 USD bleibt sinnvoll; später zusätzliche Warnungen Richtung 50 USD und GitHub-Kosten separat berücksichtigen.

Keine GPU-Instanzen, NAT Gateways oder dauerhaften Datenbanken ohne begründeten Bedarf. Nutzungs- und Aufbewahrungsgrenzen bewusst festlegen. Die Free-plan-Laufzeit endet laut bisheriger Anzeige am 6. Mai 2027; Weiterbetrieb rechtzeitig planen. Stockholm bleibt gesetzt; kein stilles Upgrade.

## Ausbauplan – spätere Ideen verbindlich festhalten

Diese Punkte werden nicht stillschweigend vergessen oder als bereits fertig bezeichnet. Nach jeder größeren Etappe gemeinsam priorisieren und Status/Nachweis ergänzen. **Zielumfang** bedeutet vereinbartes Abschlussziel; **Ausbau** bedeutet bewusst später prüfbare Idee, keine Pflicht zur sofortigen Umsetzung.

| ID | Idee | Einordnung / Voraussetzung | Status |
|---|---|---|---|
| Z1 | Beide Modi: Anwendungslogik und Pipelinefehler | Zielumfang; zuerst je ein fester Fehler | Geplant |
| Z2 | Fehlerkarten und eigener Code-Editor | Zielumfang; begrenzte Bereiche, Sandbox vor freier Vorschau | Geplant |
| Z3 | Echte PRs, automatisches Approval/Merge, eigenes Preview pro Lauf | Zielumfang; geschützte Checks, getrennte Identitäten | Geplant |
| Z4 | Jira-Ticket, Confluence-Bericht und öffentliche eigene Ansicht | Zielumfang; lokale Adapter zuerst, reale APIs danach | Geplant |
| Z5 | Anonyme Nutzung, Architekturansicht, Homepage-Fallstudie | Zielumfang; Kosten-/Nutzungskonzept vor Veröffentlichung | Geplant |
| A1 | Menschliche Freigabe als zweite Betriebsart | Gleiche Checks; wartet auf berechtigten Reviewer, kein Besucherzugriff nötig | Vorgemerkt |
| A2 | Pipeline: falsches Arbeitsverzeichnis | Ergänzende Fehlerkarte und unabhängige Prüfung | Vorgemerkt |
| A3 | Pipeline: falscher npm-Build-Befehl | Scriptnamen mit package.json abgleichen | Vorgemerkt |
| A4 | Pipeline: fehlende Job-Abhängigkeit/Artefaktübergabe | Nur begrenzt freigegebene Felder, keine Rechteänderung | Vorgemerkt |
| A5 | Anwendung: TypeScript-Typfehler / falscher Dateipfad | Zusätzliche Diagnosefälle | Vorgemerkt |
| A6 | Sortierung: schwere Pakete und gesperrte Förderwege | Fachliche Regeln und Tests erweitern | Vorgemerkt |
| A7 | Sortierung: gesperrte Station und Ausweichroute | Simulation und Routingtests erweitern | Vorgemerkt |
| A8 | Sortierung: Expresspriorität ohne dauerndes Zurückstellen normaler Pakete | Zeit-/Reihenfolgetests notwendig | Vorgemerkt |
| A9 | Sortierung: unbekanntes Ziel zur manuellen Prüfung | Zusätzliche Station und fachliche Regel | Vorgemerkt |
| A10 | RAG über Projektregeln, Runbooks und Reparaturanleitungen | Etappe 7: Chunking, Embeddings, Suche, Quellen und Nutzenvergleich | Geplant |
| A11 | Verwaltete Bedrock Knowledge Bases / Vektorspeicher vergleichen | Nur nach eigener RAG-Übung; Region und Kosten prüfen | Vorgemerkt |
| A12 | MCP und Agentenframework evaluieren | Nach nachvollziehbarer eigener Werkzeugschleife | Vorgemerkt |
| A13 | Vergleich mit/ohne zusätzlichen Kontext bzw. RAG | Gleiche Aufgaben; Qualität, Zeit und Kosten messen | Vorgemerkt |
| A14 | Modellvergleich und optional LLM als Evaluator | Geschützte Tests bleiben maßgeblich; Kosten-/Qualitätsvergleich | Vorgemerkt |
| A15 | Live-Streaming/SSE/WebSockets statt Polling | Nur bei messbarem Nutzen und passendem Budget | Vorgemerkt |
| A16 | Aufgezeichneter, klar gekennzeichneter Beispieldurchlauf | Einstieg ohne Wartezeit und Ersatz bei vollem Kontingent | Geplant |
| A17 | Architekturansicht mit hervorgehobenen aktiven Komponenten | Echte Ereignisse als Grundlage | Geplant |
| A18 | Fallstudie mit CDK-Code, Tests, Kosten, Latenzen und gemessener Reparaturquote | Nur belegte Ergebnisse, keine erfundenen Erfolgswerte | Geplant |
| A19 | Separate Subdomain und optional iframe-Einbettung | Homepage und Origin-/Einbettungsregeln vorher prüfen | Geplant |
| A20 | CI für das Workshop-Projekt separat von Besucherläufen | Entwicklungscode/CDK testen; geschützte Release-Pipeline | Geplant |
| A21 | Standardisierte wiederverwendbare Komponenten und weiterführende CDK-Tests | Bei praktischem Nutzen durch Codex erzeugen; Entwurfsentscheidungen verstehen, keine unnötigen Abstraktionen | Vorgemerkt |
| A22 | Neue Fehlerszenarien eigenständig hinzufügen | Etappe 10: mit KI selbst steuern; Erfolgskriterien, Verifikation und Diagnose erklären | Geplant |
| A23 | Terraform/CDK-Unterschied am Budget nachvollziehen | Budget verbindlich Terraform, Anwendung CDK; keine doppelte Ressourcenverwaltung | Entscheidung getroffen; Umsetzung vorbereitet |
| A24 | Optionale Kubernetes-Deploymentvariante | Lokal oder zeitweise EKS; separater Kostencheck und Rückbau, kein dauerhaftes EKS im 20–50-USD-Grundbetrieb | Vorgemerkt |

Frühere Produktideen (reines Chatfenster, Betriebsassistent, Angebotsvergleich oder Kanban als zu reparierende App) wurden durch dieses Ziel ersetzt. Sie sind keine zusätzlichen Lieferpflichten. CodeBuild/Step Functions sind ausdrücklich nicht der gewählte Pipelinepfad. Die Tabelle bewahrt die passenden Ausbauideen, ohne verworfene Ansätze wieder einzuführen.

## Persönliche Kompetenzmatrix

Nach jeder Etappe Datum, Nachweis und offene Fragen ergänzen. „Selbst“ bedeutet fachlich steuern, erklären und beurteilen können; KI-generierter Code und KI-gestützte Fehlersuche sind erlaubt. Bewertet wird Systemverständnis, nicht das Schreiben ohne Hilfsmittel.

| Thema | Neu gesehen | Mit Hilfe umgesetzt | Selbst erklärbar und änderbar | Selbst debuggt | Nachweis / offene Frage |
|---|---|---|---|---|---|
| Account, Rollen und temporäre Credentials | | | | | |
| TypeScript, Projektstruktur und Tests | | | | | |
| Terraform-Budget, CDK und CloudFormation | | | | | |
| Bedrock, Kontext und strukturierte Ausgaben | | | | | |
| Tool-Nutzung und Agentenschleife | | | | | |
| Isolation und Patchprüfung | | | | | |
| Geschützte Tests und KI-Evaluation | | | | | |
| GitHub Actions, PR, Approval und Deployment | | | | | |
| Jira-/Confluence-Werkzeuge und konsistente Dokumentation | | | | | |
| RAG und Embeddings | | | | | |
| Observability, Wiederanlauf und Kosten | | | | | |
| Weboberfläche und Website-Anbindung | | | | | |

Eine spätere Profilformulierung, sofern umgesetzt: „Eigenprojekt: Pipeline-Reparaturdemo mit GitHub Actions und Amazon Bedrock; kontrollierte Reparatur von Anwendungs- und Pipelinefehlern, echte Reparatur-PRs, unabhängige Prüfung, Jira-/Confluence-Integration und Weboberfläche; Infrastruktur über AWS CDK/TypeScript, Evaluation und Betriebsmonitoring.“ Nur tatsächlich fertiggestellte Bestandteile nennen.

## Referenzen und Prüfung bei der Umsetzung

- GitHub-App-Berechtigungen: https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app
- GitHub-Eventauslösung: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
- GitHub-Webhook-Signaturen: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
- GitHub-Workflowstart per API: https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
- GitHub Auto-Merge: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request
- GitHub-Reviews: https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request
- GitHub-Actions-Sicherheit: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub OIDC mit AWS: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
- VM-basierte GitHub-Runner: https://docs.github.com/en/actions/concepts/runners/github-hosted-runners
- GitHub-Rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- Docker-Ausführungsoptionen: https://docs.docker.com/engine/containers/run/
- GitHub-Abrechnung: https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Jira API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/
- Confluence API: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/
- Atlassian-Free-Pläne: https://www.atlassian.com/software/free

- CDK-Grundlagen: https://docs.aws.amazon.com/cdk/v2/guide/home.html
- Node.js-Unterstützung: https://docs.aws.amazon.com/cdk/v2/guide/node-versions.html
- CDK-Bootstrap: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html
- Terraform-Budgetressource: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/budgets_budget
- Frühere CDK-Budgetressource (nicht mehr verwendet): https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_budgets.CfnBudget.html
- Projektregionen: https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html
- Unterstützte Dienste: https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html
- CLI-Login und SDK-Kompatibilität: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html
- Bedrock-Modellzugang: https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
- Bedrock-Preise: https://aws.amazon.com/bedrock/pricing/
- Kostenwarnungen: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html

Konkrete APIs, Preise, Dienste und Berechtigungen beim jeweiligen Implementierungsschritt anhand offizieller Dokumentation und des tatsächlichen Accounts prüfen. Der Architekturentwurf ist noch keine getestete Bereitstellung.
