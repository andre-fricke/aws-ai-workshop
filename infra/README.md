# Workshop-Infrastruktur

- **Globales Budget:** Terraform unter [budget/](budget/README.md); direkte
  Budgets-API in `us-east-1`, kein CloudFormation-Stack und kein CDK-Bootstrap.
- **Anwendung:** CDK/TypeScript in diesem Verzeichnis, Region `eu-north-1`.
  `bin/infra.ts` instanziiert `WorkshopAppStack`; `lib/infra-stack.ts` ist zunächst
  ein leerer Platzhalter. Der frühere CDK-Budget-Stack ist entfernt und nicht
  deployt worden. Es gibt keine Budgetressource mehr in der CDK-App.

Budget und Anwendung haben getrennte Zustände und Lebenszyklen. Der Rückbau der
Anwendung darf die Budgetwarnungen nicht entfernen. Keine Ressource durch beide
Werkzeuge verwalten. Für einen echten Budgetplan und Apply siehe `budget/README.md`.
Cloudänderungen benötigen weiterhin eine konkrete Freigabe gemäß AGENTS.md.

## Lokale CDK-Prüfungen

```bash
npm run build
npx --no-install cdk list --no-lookups
```

Der leere Stack benötigt keine Lookups oder AWS-Anmeldung. Eine Synthese mit
aktiver CloudFormation-Validierung meldet derzeit erwartungsgemäß F0001
(keine Ressourcen). Den Platzhalter nicht deployen und keine Dummy-Ressource
nur zum Bestehen dieser Prüfung ergänzen. Sobald echte Anwendungsressourcen
vorliegen, gehört `cdk synth --no-lookups` wieder zur lokalen Prüfung. Beim Prüfen Credentials
und Profilzugriff deaktivieren. Die App kann sich später ändern: vor jedem lokalen
Syntheseablauf auf SDK-Aufrufe, Assets und Lookups prüfen. Es gibt aktuell keine
CDK-Ressourcen und keine dazugehörigen CDK-Tests mehr. Künftige Funktionen erhalten
passende Tests. Vor einem späteren Deployment Bootstrap-Anforderungen, Ressourcen,
Rechte und Kosten gesondert prüfen. Keine Deployments aus dieser Anleitung ableiten.
