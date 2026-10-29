# Defenseclaw_Tools_TP

Boîte à outils du TP **DefenseClaw** : des skills et des serveurs MCP malveillants prêts à l'emploi, pour s'entraîner à les scanner sans avoir à les créer.

> ⚠️ Ces fichiers contiennent de vraies charges d'attaque (reverse shell, crontab, exfiltration…). À utiliser **uniquement dans la VM du TP**.

## Contenu

```
skills/
├── malicious_skills_detected_by_regex/   skills détectés par le scanner (règles regex)
├── malicious_skills_detected_by_judge/   skills qui passent le regex, à faire attraper par le juge LLM
└── safe_skills/                          skills légitimes (pour vérifier l'absence de faux positifs)

mcp/
├── malicious_mcp_detected_by_yara/       serveurs MCP détectés par YARA (outils piégés)
└── malicious_mcp_detected_by_judge/      serveurs MCP qui passent YARA (ressources et prompts piégés)

guardrail/
├── README.md                             structure des règles du guardrail
└── keepass-rule.yaml                     exemple de règle : protéger le fichier Keepass.db

journalisation/
├── README.md                             comment importer le dashboard dans Grafana
└── dashboard-defenseclaw-simple.json     dashboard simple : règles, moteur, sévérité, cible
```

## Objectifs du TP

1. **Scanner des skills** : `defenseclaw skill scan <dossier-du-skill>`, avec et sans juge LLM.
2. **Scanner des MCP** :
   - `mcp01` à `mcp04` (stdio) : `mcp-scanner --analyzers yara stdio --stdio-command python --stdio-arg <fichier.py>`
   - `mcp05` à `mcp07` (HTTP/SSE) : lancer `python mcp0X.py`, puis `mcp-scanner --analyzers yara resources --server-url http://127.0.0.1:<port>/sse`
     (`mcp05` : port 8001, `mcp06` : port 8002, `mcp07` : port 8005, avec la commande `prompts` à la place de `resources`).
3. **Manipuler le guardrail** : lire [`guardrail/README.md`](guardrail/README.md), puis ajouter `keepass-rule.yaml` à `sensitive-paths.yaml` et comparer l'accès à un fichier `Keepass.db` avec et sans guardrail.
4. **Journalisation** : importer le dashboard dans Grafana en suivant [`journalisation/README.md`](journalisation/README.md).
