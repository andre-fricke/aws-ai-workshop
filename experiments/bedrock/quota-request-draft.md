# Bedrock-Quoten: Prüfnachweis und Antragsentwurf

Stand: 9. November 2026. **Supportfall `179423481400635` laut André manuell eingereicht.**
Bedrock-Inferenz bleibt bis zur Klärung blockiert. Den Fall nicht erneut absenden;
keinen parallelen Quotenantrag erstellen. Nächster Schritt: Antwort im bestehenden
Fall prüfen und Accountfreischaltung sowie effektive Quoten klären.
Der aktuelle AWS-Fallstatus wurde nicht ausgelesen. Der folgende Antragstext ist
die vorbereitete Referenz; der tatsächlich eingereichte Wortlaut wurde nicht
erneut aus der Console abgerufen. Keine Credentials oder Supportkorrespondenz
in dieser Datei veröffentlichen.

## Frühere API-Versandprüfung vor der manuellen Einreichung

Am 9. November 2026 wurde ausdrücklich genehmigt, genau diesen einen Fall nach
Duplikatprüfung per verfügbarer API zu erstellen. Der bestehende Accountzugang
wurde per STS bestätigt, anschließend genau eine lesende `DescribeCases`-Abfrage
am offiziellen Support-Endpunkt `https://support.us-east-1.amazonaws.com`
ausgeführt, mit aufgelösten Fällen und ohne Kommunikationsinhalte.

- Ergebnis: HTTP 400, `SubscriptionRequiredException`.
- AWS-Meldung: `Amazon Web Services Premium Support Subscription is required to use this service.`
- Request-ID: `f8a768d7-4f95-40a4-a6b5-5233d1b60acc`; `RetryAttempts=0`.
- **Case-ID: keine — kein Fall erstellt.**
- **Versandstatus: NOT_SUBMITTED_API_UNAVAILABLE.** Dies ist ein lokaler
  Bearbeitungsstatus, kein AWS-Case-Status.
- Duplikatprüfung: nicht möglich; bestehende gleichartige Fälle damit unbekannt.
- Kein `CreateCase` aufgerufen; weder erfolgreicher noch unklarer Versandversuch.
  Kein Retry, zusätzlicher Quotenantrag, Support-Upgrade oder sonstige AWS-Änderung.

Die offizielle Support-API-Dokumentation verlangt einen unterstützten bezahlten
Supportplan für `DescribeCases` und `CreateCase`. Eine öffentlich dokumentierte
alternative API für Project Support in AWS Settings wurde nicht festgestellt.
Die Berechtigung zur Console-Nutzung unter Basic Support bedeutet keinen
entsprechenden Support-API-Zugang. Zudem unterstützt `CreateCase` laut Referenz
keine Service-Limit-Anträge; deshalb kein Umdeuten des Falls in einen separaten
Quota-API-Antrag.

**Historische Console-Übergabe (inzwischen manuell erledigt):** In AWS Settings unter **Support** zuerst vorhandene Fälle
auf den unten angegebenen Betreff sowie Bedrock/Nova Lite/Accountfreischaltung
prüfen. Bei passendem Fall keinen neuen erstellen. Nur wenn kein gleichartiger
Fall besteht: **Project support → Create case**, freigegebenen **Subject** und
**Description** unverändert übernehmen und einmal **Create case** wählen.
Danach Case-ID und Status ablesen. Bei unklarer Bestätigung zuerst zur Fallliste
zurückkehren und nachsehen; nicht erneut blind absenden. Kein **Start trial**.

Lokaler maschinenlesbarer Nachweis (Git-ignoriert):
`runs/bedrock-routing/support-api-check.json`.

## Tatsächlich angewendete Werte

Profil `andre-ai-lab`, Account `331001679034`, Region Stockholm (`eu-north-1`).
Quelle: zunächst `ListServiceQuotas`, danach jede unten genannte Quote einzeln
mit `GetServiceQuota` bestätigt; keine öffentlichen Defaultwerte als Accountwerte
ausgegeben. Rohdaten lokal Git-ignoriert in `runs/bedrock-routing/quota-review.json`.

| Quotenname laut API | Quota-Code | Angewendeter Wert | Adjustable | Fachlicher Umfang |
|---|---|---:|---|---|
| On-demand model inference tokens per minute for Amazon Nova Lite | `L-70423BF8` | 0 | false | Nova Lite, Account, Region; Eingabe und Ausgabe zusammen |
| On-demand model inference requests per minute for Amazon Nova Lite | `L-E386A278` | 0 | false | Nova Lite, Account, Region |
| Cross-Model Max Tokens Per Day | `L-E3F10727` | 150.000.000 | false | Alle unterstützten Modelle zusammen, Account, Region |
| Model invocation max tokens per day for Amazon Nova Lite (doubled for cross-region calls) | `L-45E0AD92` | 0 | false | Zusätzlich angezeigtes modellbezogenes Nova-Lite-Tageslimit |
| Cross-region model inference tokens per minute for Amazon Nova Lite | `L-7C42E72A` | 0 | true | Nova Lite, Account, Region; AWS-Einstiegsquote für kombinierten Antrag |

Alle fünf Antworten enthalten `QuotaAppliedAtLevel=ACCOUNT` und
`GlobalQuota=false`. ACCOUNT bedeutet hier, dass der Wert für diesen Account
gesetzt ist; es bedeutet nicht, dass jede Quote alle Modelle umfasst.
Die Unterscheidung ergibt sich aus Name und Beschreibung der Quote.

**Befund:** Modellbezogene Nullquoten, aber keine Nullquote beim gelesenen
modellübergreifenden Tageslimit. 150 Mio. sind kein Restkontingent oder
Verbrauchszähler. Laut AWS wird das Cross-Model-Tageskontingent preisgewichtet
geschätzt; es ist nicht ohne Weiteres mit gleich vielen Nova-Lite-Texttokens
oder einem USD-Budget gleichzusetzen.

AWS beschreibt für das zusätzlich angezeigte Nova-Lite-Tageslimit ausdrücklich:
`not applicable in case of approved TPM increase`. Die aktuelle Runtime-Dokumentation
beschreibt das gemeinsame Cross-Model-Tageslimit. Beide Angaben transparent
beibehalten und AWS um Klärung bitten. Aus dem generischen HTTP-429-Fehler allein
lässt sich nicht sicher bestimmen, welche interne Prüfung die Anfrage abwies.
Er belegt insbesondere keine accountweite Nullquote.

## Dokumentierter Empfänger und Antragsweg (bereits manuell eingereicht)

**AWS Project Support / Account Support (Basic Support), über AWS Settings.**
Anfrage zur Accountfreischaltung mit Bitte um interne Weiterleitung an das
Amazon-Bedrock-Quotenteam. Kein zusätzlicher Service-Quotas-Antrag parallel.
Dies ist die Einordnung des hier vorliegenden Accountzugangsproblems; AWS muss
bestätigen, ob und wie das bestehende Accountmodell dafür freigeschaltet werden kann.

Die offizielle Dokumentation zum neuen AWS-Erlebnis nennt als kostenlosen
Account-/Projekt-Supporteingang:

1. Als bisheriger Builder-ID-/Projektbenutzer bei https://settings.aws.com anmelden.
2. Den betroffenen Projektkontext **Blank Canvas** verwenden und Account-ID
   `331001679034` unter **Project → Overview → Additional Info** kontrollieren.
3. **Support → Project support → Create case** öffnen.
4. **Subject** und **Description** mit dem unten vollständig angegebenen Text
   befüllen. Ein vorhandenes Kosten-/Supportangebot nicht aktivieren.
5. Die manuelle Einreichung ist inzwischen gemeldet: Fall `179423481400635`.
   Den bestehenden Fall zur weiteren Kommunikation öffnen; **Create case**
   nicht erneut verwenden.

Die Dokumentation garantiert nicht, dass Project Support den Bedrock-Anteil
selbst bearbeitet; deshalb um interne Weiterleitung im selben Fall bitten.
Basic Support deckt Accountfragen ab. Reguläre technische Supportfälle sind
unter Basic Support nicht verfügbar; ein kostenpflichtiges Abo oder **Start trial**
ist hier nicht vorgesehen. Die allgemeine AWS-Supportdokumentation nennt
Service-Limit-Anträge als für alle Kunden verfügbar.

Der normale Bedrock-Quotenweg führt kombinierte Anträge über die änderbare
Cross-Region-TPM-Quote. Das ist keine zusätzliche Freischaltung und kein Beweis,
dass direkte Quoten automatisch gesetzt werden. **Der frühere numerische
Cross-Region-Einstiegsantrag wird durch diesen Accountklärungsfall ersetzt**:
Es wird keine Cross-Region-Quota-Erhöhung verlangt. Wenn AWS einen anderen
Eingang fordert, die Antwort im bestehenden Fall nutzen und vor weiterem
Absenden den konkreten Weg neu abstimmen; keine zwei parallelen Fälle erzeugen.

Keine Genehmigungszusage oder Bearbeitungsfrist. Codex hat keinen Fall über die
API erstellt; die manuelle Einreichung wurde vom Nutzer bestätigt. Keine weiteren
Modellaufrufe, Upgrades, Supportabos, parallelen Quotenanträge oder
Kapazitätsreservierungen durch Codex ausgeführt.

## Vollständiger Antragstext (Englisch)

**Subject:** Bedrock account enablement and small Nova Lite quota request — eu-north-1

**Description:**

Hello AWS Support,

Please review Bedrock account enablement and a small inference quota allocation for:

- AWS account: 331001679034
- Project: Blank Canvas, using the new AWS experience and Free plan
- Region: eu-north-1 (Europe / Stockholm)
- Model: amazon.nova-lite-v1:0
- API: Converse through the direct bedrock-runtime endpoint in Stockholm

Do I need any additional account-level activation, verification, or Bedrock
inference enablement before I can use this model? Please identify any account
restriction or provisioning step that explains the zero throughput quotas,
and confirm whether it can be resolved within my existing account and Free plan.

Confirmed findings from read-only API checks on 9 November 2026:

- Several models report AUTHORIZED, with regional and entitlement availability.
  Applied throughput quotas are nevertheless zero for every candidate checked.
- Nova Lite agreement, entitlement and regional availability report AVAILABLE.
- Nova Lite on-demand tokens/minute: 0 (L-70423BF8).
- Nova Lite on-demand requests/minute: 0 (L-E386A278).
- Nova Lite model-specific maximum tokens/day: 0 (L-45E0AD92).
- Cross-Model Max Tokens Per Day: 150,000,000 (L-E3F10727).
  This shared account/Region quota is not zero; no increase to it is requested.

One direct Nova Lite Converse attempt in Stockholm returned HTTP 429,
ThrottlingException: "Too many tokens per day, please wait before trying again."
Request ID: ebd73222-fedd-4d96-941a-3f821a3b3f1e
The request body was 2,938 UTF-8 bytes, maxTokens was 512, and SDK retries were
disabled. No model response or token usage was returned.

Please enable this small allocation for direct Nova Lite inference in Stockholm:

- 10,000 tokens per minute (input and output combined).
- 2 requests per minute.
- 100,000 model tokens per day, only if a separate model-specific daily quota
  remains necessary. Its API description says it is not applicable after an
  approved TPM increase; please clarify which daily limit will apply.

The use case is a personal educational workshop: one developer manually requests
and reviews a JSON repair suggestion for a small TypeScript routing defect.
There will be one concurrent request, initially at most 20 manual attempts/day,
small text-only inputs, and at most 512 output tokens per request. Inputs contain
synthetic requirements, public demo code and selected test logs, without customer
data or credentials. No public or autonomous inference workload is enabled.

Please handle account enablement and quota review in this single case, routing it
internally to the Bedrock quota team if needed. No model change, cross-region
inference, cross-region quota increase, paid support subscription, provisioned
throughput, capacity reservation, or account upgrade is requested or authorized.
If this allocation is unavailable on the existing plan, please explain the
restriction before suggesting any paid change.

Thank you.

## Offizielle Quellen

- [Support für das neue AWS-Erlebnis: Basic Support und AWS Settings](https://docs.aws.amazon.com/accounts/latest/reference/access-aws-support.html)
- [DescribeCases: erforderlicher Supportplan](https://docs.aws.amazon.com/awssupport/latest/APIReference/API_DescribeCases.html)
- [CreateCase: erforderlicher Supportplan und keine Service-Limit-Anträge](https://docs.aws.amazon.com/awssupport/latest/APIReference/API_CreateCase.html)
- [Account-/Billing- und Service-Limit-Fälle; Grenze zu Technical Support](https://docs.aws.amazon.com/awssupport/latest/user/case-management.html)
- [Projektregion und Account-ID in AWS Settings kontrollieren](https://docs.aws.amazon.com/accounts/latest/reference/project-regions.html)
- [Bedrock-Runtime-Quoten und regulärer Quotenantragsweg](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-runtime.html)
- [Service Quotas: Erhöhung beantragen](https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html)
