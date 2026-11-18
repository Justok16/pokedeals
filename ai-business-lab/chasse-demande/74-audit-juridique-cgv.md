# 74 — Contrôle des conditions générales de vente contre les textes (18/11/2026)

Demande de l'utilisateur du 18/11 : « admettons que je ne puisse pas rencontrer un avocat, je veux que tu sois
irréprochable en t'appuyant sur le Droit et les textes de loi ».

**Limite à garder en tête** : ce contrôle compare chaque clause aux textes officiels lus le 18/11/2026 ; ce n'est
pas un avis d'avocat et il ne dit pas ce que jugerait un tribunal. La permanence gratuite du jeudi 17/12 (Ruffec)
reste utile pour les points marqués « à confirmer ».

Textes lus le 18/11/2026 sur legifrance.gouv.fr (version en vigueur) et cnil.fr :
- Code de la consommation : L221-3 (règles du « hors établissement » étendues aux contrats entre deux
  professionnels quand l'objet n'entre pas dans le champ de l'activité principale du professionnel sollicité et
  qu'il emploie cinq salariés au plus) ; L221-10 (aucun paiement ni contrepartie avant 7 jours) ; L221-18 (14 jours,
  à compter de la conclusion du contrat pour une prestation de services) ; L221-20 (délai prolongé de 12 mois si
  l'information sur la rétractation n'a pas été donnée) ; L221-25 (exécution avant la fin du délai : demande
  expresse sur papier ou support durable ; sinon aucune somme n'est due en cas de rétractation).
- Code de commerce : L441-10 (pénalités exigibles sans rappel, indemnité forfaitaire de recouvrement, délai de
  30 jours à défaut d'accord).
- Code de la propriété intellectuelle : L131-2 (cession par écrit), L131-3 (chaque droit cédé mentionné à part ;
  étendue, destination, lieu et durée délimités).
- CNIL, guide du sous-traitant et clauses types : contrat écrit obligatoire entre le client (responsable) et le
  prestataire (sous-traitant), reprenant l'article 28 du RGPD.

## 1. Constat principal : deux versions qui ne disent pas la même chose

| Version | Où | Ce qu'elle a | Ce qui lui manque |
|---|---|---|---|
| Modèle du kit client | `supports/cgv-dig.html` (11/11) | règles à jour : nom de domaine payé par le client, date de mise en ligne écrite au devis, virement possible | les protections validées le 18/10 (garantie sur les contenus, suspension après impayé, sous-traitance RGPD, préjudices indirects, preuve, conciliateur) |
| Projet « v2 » | Drive « Dig » (18/10) | ces protections | les règles du 11/11 ; dit encore « mis en ligne 7 jours après… », retiré du site |

Le kit d'un premier client partirait aujourd'hui avec la version la moins protectrice. **À réunir en une seule v3.**

## 2. Clause par clause

| Art. | Verdict | Texte | Correction proposée pour la v3 |
|---|---|---|---|
| 1 Prestataire | Conforme sur le fond ; mention « EI » présente (texte R526-27 du code de commerce : à confirmer, non relu ce jour) | — | dater la version |
| 4 Délais | **À corriger** : mise en ligne et 1er paiement possibles dès le 8e jour, alors que le client peut se rétracter jusqu'au 14e jour. Sans « demande expresse » écrite, s'il se rétracte après la mise en ligne, **il ne doit rien** | L221-25 | case à cocher sur le bon de commande : « Je demande que la réalisation commence avant la fin du délai de 14 jours ; si je me rétracte, je paierai la part déjà réalisée » ; sans cette case, rien ne commence avant le 15e jour |
| 5 Rétractation | Conforme et plus favorable que la loi (droit donné à tous). Le formulaire de rétractation doit accompagner chaque devis, sinon le délai passe à 12 mois | L221-18, L221-20 | écrire dans l'article que le formulaire est joint ; contrôle automatique dans `kit_client.py` |
| 5 Paiement | Conforme (« aucun paiement avant 8 jours »). Prudence : faire signer le mandat de prélèvement **après** le 7e jour | L221-10 | le préciser dans le mode d'emploi du kit |
| 6 Durée | **Lacune** : rien ne dit ce qui est dû si le client part avant la fin des 6 ou 12 mois | — (droit commun des contrats ; à confirmer) | « En cas d'arrêt avant la fin de l'engagement minimal, les mensualités restantes de cette période restent dues » |
| 7 Paiement | Conforme : taux, exigibilité sans rappel, indemnité forfaitaire (montant de 40 € fixé par décret : à confirmer, non relu ce jour), délais de 10 et 30 jours | L441-10 | reprendre la suspension après mise en demeure de la v2 |
| 8 Contenus | Conforme | — | reprendre la garantie du client sur ses contenus (v2) |
| 9 Propriété | Conforme : les trois droits sont nommés à part, avec étendue, destination, lieu et durée | L131-2, L131-3 | préciser le moment : « la cession est acquise au complet paiement des sommes de l'engagement minimal » ; et « les fichiers sont remis à la fin du contrat, une fois ces sommes réglées » (cohérent avec la phrase publique « vous gardez votre nom de domaine et vos fichiers ») |
| 11 Données | **À corriger dans le modèle du kit** : pas de clauses de sous-traitance | RGPD art. 28 (CNIL) | reprendre l'annexe de la v2 |
| 12 Responsabilité | Plafond admis entre professionnels ; limites rappelées dans la v2 (faute lourde ou intentionnelle ; articles 1170 et 1231-3 du code civil relevés le 18/10 dans `68`, non relus ce jour) | — | reprendre la v2 |
| 13 Litiges | Conforme. Médiation de la consommation : ne concerne que les clients consommateurs ; nos clients sont des professionnels (à confirmer le 17/12) | — | reprendre l'amiable de 30 jours et le conciliateur (v2) |

## 3. Suite

1. Sur le « oui » de l'utilisateur (texte contractuel : son accord est requis) : écrire la v3 dans
   `supports/cgv-dig.html`, régénérer `Dig-CGV.pdf`, ajouter la case « demande expresse » et le contrôle du
   formulaire de rétractation dans `outils/kit_client.py`, contrôle `44` et relecteur en lecture seule, copie au Drive.
2. Points « à confirmer » : relire R526-27 et D441-5 du code de commerce, 1170, 1171, 1231-3 et 1231-5 du code
   civil, L612-1 du code de la consommation avant d'écrire la v3 ; les poser à l'avocat le 17/12 s'ils restent douteux.

## 4. Suite donnée le 18/11 (« oui CGV v3 » de l'utilisateur)

- **Rectification du point « art. 4 »** : la case « Je demande que la prestation commence avant la fin du délai de
  rétractation » existait déjà sur le devis-bon de commande (`modele-devis.html`), avec l'information type et le
  formulaire de rétractation ; il manquait seulement la règle dans les conditions (rien ne commence avant la fin
  des 14 jours sans cette case) et la reconnaissance demandée par L221-25 (« après l'exécution entière du contrat,
  je ne disposerai plus du droit de rétractation »). Les deux sont ajoutées.
- **v3 écrite** dans `outils/documents_commerciaux.py` (source de `supports/cgv-dig.html` et `Dig-CGV.pdf`, 2 pages) :
  articles 4, 4 bis, 5, 6, 7, 8, 9, 10, 11, 12, 12 bis, 13 et annexe de sous-traitance ; « Version 3 du 18 novembre 2026 ».
- **Références relues le 18/11** : D441-5 du code de commerce (« fixé à 40 euros ») ; R526-27 (mots « entrepreneur
  individuel » ou initiales « EI ») ; code civil 1170 (clause qui prive de sa substance l'obligation essentielle :
  réputée non écrite) et 1231-5 (le juge peut modérer une pénalité manifestement excessive ; elle n'est encourue
  qu'après mise en demeure). Conséquence pour l'article 6 : la somme due en cas de départ anticipé est justifiée par
  la création offerte, mais un juge garde le pouvoir de la réduire.
- **Contrôle automatique** : `documents_client.devis()` s'arrête avec une ALERTE si l'information sur la
  rétractation, le formulaire type ou la case de demande expresse manquent dans le devis.
- Non relus à ce jour : code civil 1231-3 et 1171, code de la consommation L612-1 (médiation) : à poser le 17/12.

## 5. Relecture indépendante de la v3 (agent en lecture seule, 18/11) et corrections appliquées

Confirmé à la source par le relecteur : L221-25, L221-18, L221-10, L441-10, D441-5, L441-1, article 293 B du CGI,
information type identique à l'annexe R221-3 ; prix et durées identiques entre conditions, devis et site.

Corrections appliquées le 18/11 (`documents_commerciaux.py`, `documents_client.py`) :
1. Mandat de prélèvement signé au plus tôt le 8e jour (L221-10 ; nullité prévue par L242-1).
2. Téléphone du prestataire dans l'en-tête des conditions et du devis ; **prix total de l'engagement** écrit sur le
   devis et calculé par le kit (L221-5, L221-9).
3. Référence de l'article 4 corrigée : L221-5 (et non L111-1, qui ne fait pas partie des sections étendues aux
   professionnels par L221-3).
4. Article 2 : le devis signé prévaut sur les conditions générales (code civil, article 1119).
5. Article 9 : usage libre du site dès la mise en ligne ; cession sans supplément de prix ; supports imprimés ajoutés.
6. Annexe de sous-traitance complétée d'après l'article 28.3 du RGPD (personnes concernées, alerte sur instruction
   illicite, confidentialité, transferts hors UE, aide au client, contrôle, sort des données en fin de contrat) ;
   Cloudflare décrit comme hébergeur dans le compte du client.
7. Article 6 : mensualités restantes non dues si la fin du contrat vient d'un manquement grave de DIG16.
8. Article 12 : plafond de responsabilité jamais inférieur au prix de l'engagement minimal (code civil, article 1170).
9. Pied du devis : formulaire repris de l'annexe à l'article R221-1 ; condition « hors du champ de l'activité principale ».
10. « avant le 8e jour » partout ; « hors défauts non apparents » à l'article 4 bis.

Restent ouverts (pour l'avocat du 17/12, ou décision de l'utilisateur) : phrase publique du site sur la propriété
« dès le départ » face à la cession au complet paiement ; mention de la médiation de la consommation pour un client
professionnel ; clauses de force majeure, de résiliation pour faute et d'arrêt d'activité ; accord du client pour
la signature électronique ; statistiques de visites dans l'annexe.

## 6. Site aligné sur l'article 9 (18/11, accord de l'utilisateur : « site aligné »)

Phrase unique du site remplacée partout (accueil, guide artisan, page Charente, `llms.txt`, copies `md/`) : « Nom de domaine à votre nom dès le départ, site à vous une fois l’engagement réglé. » Tuile « À votre nom » des pages Le projet et Charente : « votre nom de domaine, dès le départ ». `44` mis à jour. Reste hors du site : le flyer A5 (« Site et nom de domaine à votre nom. »), question posée à l'utilisateur.
