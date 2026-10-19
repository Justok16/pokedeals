#!/bin/sh
# Rappel injecté à chaque message de l'utilisateur (19/10/2026) : la vérification se fait AVANT d'agir, pas après.
# L'utilisateur : « le but c'est plutôt de vérifier avant, à chaque fois. Ce que tu ne fais pas et ça arrive souvent ».
cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"VÉRIFIER AVANT D'AGIR (règle ferme du 19/10) : 1) outil ou service utilisé en série → lire sa limite gratuite à la source et compter ce qui est déjà consommé ce mois ; 2) menu ou parcours → connaissances/parcours-verifies.md ou page d'aide lue ; 3) fait, chiffre, adresse, identifiant → vérifié à la source avant de l'écrire ; 4) « que me reste-t-il » → 64 § 0 + 69 § 5 + 61 § 1 + 68 § 5 + partages-groupes + rappels programmés ; 5) relire connaissances/lecons.md pour ce type de tâche."}}
EOF
