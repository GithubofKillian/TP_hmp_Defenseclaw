# Journalisation

Dashboard Grafana simple pour visualiser les findings de DefenseClaw : règle remontée, moteur de détection, sévérité et cible associée.

## Ajouter le dashboard

1. Lancer la stack d'observabilité (Grafana sur http://localhost:3000, identifiants `admin` / `admin`) : `defenseclaw setup local-observability up`.
2. Dans Grafana : **Dashboards → New → Import**.
3. Coller le contenu de [`dashboard-defenseclaw-simple.json`](dashboard-defenseclaw-simple.json) (ou charger le fichier), puis **Load → Import**.

Les sources de données (`defenseclaw-loki`, `defenseclaw-prometheus`) sont déjà fournies par la stack : rien d'autre à configurer.

## À savoir

- Les données viennent de DefenseClaw (événements `finding.observed` dans Loki) : il faut avoir lancé des scans avec la télémétrie active pour voir quelque chose.
- Si le dashboard est vide, élargir la période (par défaut : 24 dernières heures).
- Le panneau « Guardrail » ne se remplit que lorsque le guardrail est activé.
