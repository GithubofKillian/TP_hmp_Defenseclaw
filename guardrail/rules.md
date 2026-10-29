Les règles du guardrail sont dans /home/user/.defenseclaw/policies/guardrail/. Il y a trois profils (default, strict, permissive), on verifie lequel est actif dans config.yaml.

Format :
/home/user/.defenseclaw/policies/guardrail/<profil>/
├── rules/                  ← règles regex
│   ├── commands.yaml
│   ├── c2.yaml
│   ├── secrets.yaml
│   ├── sensitive-paths.yaml
│   ├── enterprise-data.yaml
│   ├── trust-exploit.yaml
│   ├── cognitive.yaml
│   └── local-patterns.yaml
├── judge/                  ← prompts du juge LLM
│   ├── injection.yaml
│   ├── tool-injection.yaml
│   └── pii.yaml
├── suppressions.yaml 
└── sensitive-tools.yaml 

Les décisions d'action sont séparées, dans /home/user/.defenseclaw/policies/rego/ (guardrail.rego, skill_actions.rego, admission.rego, firewall.rego, sandbox.rego, audit.rego, data.json).

Règle regex : un fichier a un en-tête version et category, puis une liste rules. Chaque règle a ces champs :
- id
- pattern (regex)
- title
- severity
- confidence (de 0 à 1)
- tags

Les commentaires YAML expliquent parfois les choix de la regex.

- id: CMD-REVSHELL-BASH
  pattern: '(?i)bash\s+-i\s+>&\s*/dev/tcp/'
  title: "Bash reverse shell"
  severity: CRITICAL
  confidence: 0.98
  tags: [execution, reverse-shell]

Autres exemples : CMD-REVSHELL-NC (netcat avec -e, CRITICAL, 0.95) et C2-WEBHOOK-SITE (HIGH, 0.90).

Juge LLM (judge/injection.yaml) : le fichier contient name, enabled et un system_prompt. Ce prompt traite l'échantillon comme des données seulement (entre <<<SAMPLE>>> et <<</SAMPLE>>>). Il définit les catégories d'attaque :
- manipulation d'instructions
- manipulation de contexte
- obfuscation
- manipulation sémantique
- exploitation de tokens

Il ajoute une liste d'exclusions, par exemple les invocations d'outils normales ou le code contenant des chaînes qui ressemblent à des instructions. Il impose aussi un seuil : « only flag if CLEAR, deliberate attempt », avec au moins deux signaux faibles.

Suppressions (suppressions.yaml) : deux listes, pre_judge_strips (motifs retirés avant le juge, avec applies_to: [pii]) et finding_suppressions (résultats écartés après coup).

Sensitive tools (sensitive-tools.yaml) : une liste tools où chaque entrée a un name, result_inspection, judge_result et parfois min_entities_for_alert.
