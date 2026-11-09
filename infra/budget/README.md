# Globales AWS-Budget mit Terraform

Dieses Verzeichnis verwaltet ausschließlich das kontoweite Budget für Account
331001679034 über die Budgets-API in `us-east-1`. Es erstellt keinen
CloudFormation-Stack. Anwendung und sonstige Infrastruktur gehören weiterhin
zur CDK-App unter `../` in Stockholm (`eu-north-1`). Eine Ressource hat genau
einen IaC-Eigentümer; das Budget darf nicht zusätzlich per CDK verwaltet werden.

## Umfang

- Ein Kostenbudget `andre-ai-lab-monthly`: 20 USD pro Monat, alle Regionen/Dienste.
- E-Mail-Warnungen bei Überschreiten von 5, 10 und 20 USD tatsächlicher Kosten.
- Credits werden nicht abgezogen; andere Kostenarten verwenden Providerdefaults.
- Keine Budget Actions, IAM-Rollen, Compute-, SNS- oder Bootstrap-Ressourcen.
- Budget ist Alerting, kein Ausgabenlimit. AWS-Abrechnung kann verzögert sein;
  GitHub-Kosten werden nicht erfasst. Reines Budgetmonitoring und Benachrichtigungen
  kosten nach der AWS-Preisliste keine laufenden Zusatzgebühren.

## Lokale Vorbereitung

Aus diesem Verzeichnis:

```bash
terraform init -backend=false
terraform fmt -check -recursive
terraform validate
terraform test
```

`init` lädt den Provider aus der Terraform Registry (Netzwerkzugriff, kein AWS).
Die Tests verwenden einen Mock-Provider und `command = plan`: kein echter
AWS-Zugriff und kein Apply. Die `.terraform.lock.hcl` gehört ins Repository.

## Erst nach gemeinsamer Besprechung: echter Plan und Apply

Profil `andre-ai-lab` verwenden; bestehendes `default` unverändert lassen.
AWS-CLI-Login-Kompatibilität des Providers wurde mit Plan und Apply bestätigt. Bei künftigem Bedarf
nur den offiziell dokumentierten Credential-Process-Weg ergänzen; keine festen
Zugangsschlüssel als Ersatz anlegen. Mögliche fremde AWS-Credential-Umgebungsvariablen
vor dem Plan prüfen, ohne deren Werte auszugeben. Provider prüft die erlaubte
Account-ID; die Ressource bindet dieselbe ID zusätzlich explizit.

Empfänger lokal setzen, beispielsweise in einer ignorierten Datei
`terraform.tfvars` mit `alert_email = "DEINE-ADRESSE"`. Nicht die Beispieladresse
aus den Tests verwenden. Die Adresse ist als sensitive markiert, steht aber im
Terraform-State und für berechtigte AWS-Budget-Leser weiterhin im Klartext.
Lokaler State ist für den einzelnen Workshop-Arbeitsplatz vorgesehen: vertraulich
aufbewahren, sichern und nie committen. Keine parallelen Applies; Remote-State
erst bei tatsächlichem Team-/Automatisierungsbedarf separat planen.

Zuerst `terraform plan -out=budget.tfplan` gemeinsam prüfen. Ein echter Plan
nutzt AWS-Lesezugriffe/Anmeldung. Erwartung: genau ein neues Budget, kein anderer
Ressourcenaufbau. Ein bereits bestehendes gleichnamiges Budget erst prüfen und
gegebenenfalls importieren statt doppelt erstellen. Plan-Datei vertraulich halten.
Erst nach konkreter Freigabe den geprüften Plan mit
`terraform apply budget.tfplan` anwenden. Änderungen an Code/Variablen erfordern
neuen Plan. Kein `-auto-approve` im Workshopablauf.

Budget-Verwaltung benötigt `budgets:ModifyBudget` und `budgets:ViewBudget`,
soweit möglich auf `arn:aws:budgets::331001679034:budget/andre-ai-lab-monthly`
beschränkt. Der Provider kann außerdem STS für die Accountprüfung verwenden.
Es werden keine Rechte durch diesen Code vergeben. Tatsächliche Schreibrechte
und Zustellung sind erst nach einem genehmigten Apply und anschließender Prüfung
bestätigt. Nach Erfolg Budget und alle drei Empfänger-/Schwellenkonfigurationen
lesen und kontrollieren; eine künftige Warnmail ist noch kein lokal testbarer Nachweis.

`terraform destroy` würde die Kostenwarnungen entfernen und benötigt eine eigene
konkrete Freigabe. Beim Rückbau der Demo Budget nach Möglichkeit erhalten.

## Prüfnachweis vom 9. November 2026

- Empfänger in ignorierter `terraform.tfvars` lokal hinterlegt (Dateirechte 0600).
- Festgeschriebener AWS-Provider 6.72.0 installiert; Lockdatei unverändert verwendet.
- `terraform fmt -check -recursive`, `terraform validate` und beide Mock-Tests erfolgreich.
- Echte lesende Budgets-Abfrage mit `andre-ai-lab`: `NotFoundException` für
  `andre-ai-lab-monthly`; damit kein gleichnamiges Budget zum Prüfzeitpunkt vorhanden.
- Echter `terraform plan -out=budget.tfplan -detailed-exitcode` erfolgreich
  (Exitcode 2: Änderungen geplant): **1 anlegen, 0 ändern, 0 löschen**.
- Provider-Anmeldung mit dem bestehenden Profil und erlaubter Account-ID erfolgreich;
  kein Credential-Process-Ersatz erforderlich.
- Gespeicherten Plan strukturiert geprüft: drei tatsächliche Kostenschwellen
  5/10/20 USD, richtige lokale Empfängervariable, Credits ausgeschlossen und
  keine Kostenfilter konfiguriert. Der Textplan blendet die sensitive
  Benachrichtigungskonfiguration aus; `cost_filter` ist dort providerbedingt
  als erst nach Apply bekannt markiert.
- Kein Apply, keine AWS-Ressourcenänderung. Schreibberechtigungen und
  E-Mail-Zustellung sind weiterhin unbestätigt. Plan-Datei vertraulich behandeln.

## Apply und AWS-Verifikation vom 9. November 2026

Nach ausdrücklicher Freigabe wurde ausschließlich der oben beschriebene
gespeicherte Plan mit `terraform apply -input=false -no-color budget.tfplan`
angewendet: **1 angelegt, 0 geändert, 0 gelöscht**. Kein neuer Plan,
keine zusätzlichen Ressourcen, kein Bootstrap und keine Konfigurationsänderung.
Der Plan ist damit verbraucht; spätere Änderungen benötigen einen neuen Plan
und eine passende Freigabe.

Anschließend über die AWS-Budgets-API lesend verifiziert:

- `DescribeBudget`: `andre-ai-lab-monthly`, Account `331001679034`,
  Kostenbudget (`COST`), `MONTHLY`, 20 USD.
- Keine `CostFilters` und keine `FilterExpression`: alle Regionen und Dienste
  des Accounts. `IncludeCredit=false`; sonstige Kostenarten entsprechen den
  Providerdefaults, einschließlich Steuern und Erstattungen.
- `DescribeNotificationsForBudget`: genau drei Warnungen mit `ACTUAL`,
  `ABSOLUTE_VALUE`, `GREATER_THAN` und Schwellen von 5, 10 und 20 USD.
- Für jede Warnung `DescribeSubscribersForNotification`: genau ein
  E-Mail-Empfänger, identisch mit der freigegebenen lokalen Adresse;
  keine SNS-Empfänger. Adresse nicht in diesen Prüfnachweis übernommen.

Erstellung und Lesezugriffe sind damit bestätigt. Die tatsächliche Zustellung
einer künftigen Warnmail wurde nicht beobachtet. Empfängerdatei, State und Plan
bleiben lokal, vertraulich und Git-ignoriert; State sichern. Keine Commits oder Pushes.

## Hintergrund der Trennung

Andrés lesende Abfrage lieferte `TypeNotFoundException` für
`AWS::Budgets::Budget` in Stockholm. CloudFormation in `us-east-1` ist laut
veröffentlichten Projektregeln gesperrt, während `budgets:*` ausgenommen ist.
Terraform verwendet die Budgets-API direkt. Der Bereitstellungsweg wurde durch
den freigegebenen Apply und anschließende Leseprüfung im bestehenden Account bestätigt.

- [Terraform-Budgetressource](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/budgets_budget)
- [AWS-Projektregeln](https://docs.aws.amazon.com/accounts/latest/reference/scps-and-rcps-for-projects.html)
- [AWS-Budgets-Preise](https://aws.amazon.com/aws-cost-management/aws-budgets/pricing/)
