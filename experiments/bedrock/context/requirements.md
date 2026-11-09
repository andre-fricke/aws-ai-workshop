# Fachliche Anforderungen für den einzelnen Reparaturvorschlag

Ein Paket hat eine unveränderliche `id: string` und ein `destination` aus
`Berlin`, `Hamburg`, `München`. Die Funktion `routeParcel` liefert eine Station:
Berlin → `berlin`, Hamburg → `hamburg`, München → `munich`.
Die ID beeinflusst das Ziel nicht. Eingabe und fachliche Tests bleiben unverändert.

Untersuche ausschließlich die mitgelieferte fehlerhafte Datei. Schlage eine
kleine Korrektur des Berliner Zweigs vor. Änderungen an Hamburg/München,
Imports, Typen, Tests, Abhängigkeiten oder Workflows sind nicht erlaubt.
Ein Vorschlag wird nur als Daten geprüft, nicht angewendet oder ausgeführt.
