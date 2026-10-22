# Product

<!-- impeccable:product-schema 1 -->

Statut : rédigé le 19/10/2026 à partir des documents du projet, **validé par l'utilisateur le 19/10/2026** (« oui la fiche PRODUCT.md me va »). Aucun témoignage, client ni chiffre inventé.

## Platform

web

## Stack

Static HTML/CSS (site `ai-business-lab/chasse-demande/site-dig/`), hébergé sur Cloudflare Pages (dig16.fr).
Polices hébergées sur le site (`/moteur/polices/`), jamais d'appel à Google Fonts. Pas de framework.

## Users

Artisans, commerçants et indépendants de Charente (Nord-Charente d'abord), souvent seuls ou petite équipe, peu à
l'aise avec internet, qui consultent surtout depuis leur téléphone. Leur besoin : être trouvés et appelés par des
clients du coin, sans gérer la technique. Public secondaire : les clients de ces artisans (sites livrés).

## Product Purpose

DIG16 crée et entretient des sites internet simples pour ces professionnels : 0 € de création sur les formules
mensuelles (dès 49 €/mois, hébergement, modifications et suivi compris), ou achat. Le site dig16.fr doit obtenir une
prise de contact : la page d'accueil refaite gratuitement, pour voir avant de décider. Succès = demandes reçues.

## Positioning

Un interlocuteur local en Charente ; le site et le nom de domaine restent au nom du client ; tarifs écrits noir sur
blanc ; modifications sous 3 jours ouvrés ; guide gratuit « quoi vérifier avant de signer » valable chez n'importe
quel prestataire.

## Operating Context

Prospection par téléphone, visites avec flyer, réseaux sociaux (Facebook, Instagram, TikTok, Threads, YouTube, X),
fiche Google. Les démos personnalisées sont montrées en direct, jamais envoyées sans accord.

## Capabilities and Constraints

- Aucune donnée personnelle de l'utilisateur ni de prospect dans le dépôt public (seule adresse : contact@dig16.fr).
- Toute affirmation du site doit rester vraie (entreprise immatriculée, prix, CGV) ; rien d'invérifié.
- Secteurs exclus des cibles : métiers aux règles de publicité strictes (alcool, tabac, jeux, santé, professions
  réglementées, immobilier, assurance, crédit, CBD).
- Avant toute mise en ligne : `python3 outils/test_pages.py` sans ALERTE (ordinateur et téléphone), puis IndexNow.
- Capacité : 15 clients maximum la première année.

## Brand Commitments

Nom commercial DIG16 (jamais « Dig » seul), domaine dig16.fr. Ton simple, direct, en français courant, sans jargon
technique ni clichés publicitaires. Le parcours professionnel et la situation personnelle du fondateur ne sont
jamais mentionnés.

## Evidence on Hand

Pas encore de client, d'avis ni de témoignage : n'en inventer aucun. Démos de démonstration marquées « entreprises
fictives ». Guide gratuit : dig16.fr/site-internet-artisan/.

## Product Principles

1. Le téléphone d'abord : appeler en un geste, lisible sans zoomer.
2. La vérité avant l'effet : chaque chiffre et chaque promesse vérifiables.
3. Le client reste propriétaire de son site et de son adresse.
4. Simple à comprendre en 5 secondes pour quelqu'un qui n'aime pas internet.

## Accessibility & Inclusion

WCAG 2.1 AA (audit axe-core après chaque refonte), cibles tactiles de 24 px minimum, public souvent âgé ou peu
technophile : texte lisible, contrastes francs.
