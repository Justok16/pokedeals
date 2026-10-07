# Kimi peut hacker n'importe quel SaaS : comment t'en protéger AUJOURD'HUI ?

Vidéo : https://youtu.be/lQKCUxrKiao · durée 22:11 · résumé Gemini (gemini-3.5-flash-lite) du 2026-10-07
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici un résumé structuré de la vidéo, en français, axé sur les aspects pratiques pour gagner de l'argent légalement grâce à l'IA et aux audits de sécurité automatisés (type "pentest") :

---

### 1. Idée principale
L'auteur explique comment il utilise des modèles d'IA non bridés (comme *Kimi K3*) pour auditer automatiquement la sécurité de SaaS (logiciels en tant que service) et y trouver des failles, souvent plus rapidement et efficacement que les modèles bridés traditionnels. Il présente une opportunité commerciale légale : proposer des services de "pentest" automatisé payants pour aider les propriétaires de SaaS à sécuriser leurs applications avant qu'un attaquant malveillant ne les exploite.

---

### 2. Outils, sites et dépôts GitHub cités

*   **Kimi K3 (Kimi AI / Modèle Kimi)**
    *   *Type :* Payant / Accès via API (selon la plateforme utilisée).
    *   *Rôle :* Grand modèle de langage (IA) non bridé, utilisé dans la vidéo pour effectuer des audits de sécurité approfondis sur du code et trouver des failles sans filtre de refus excessif.
*   **Opus (Opus 5 / Claude Opus)**
    *   *Type :* Payant.
    *   *Rôle :* Modèle concurrent (modèle bridé avec des classificateurs de sécurité) qui refuse de réaliser des audits de sécurité d'intrusion (considéré comme trop protecteur).
*   **Pentest by Melvyn**
    *   *Nom exact du site :* `pentest.melvynx.dev`
    *   *Type :* Payant (Service commercialisé par l'auteur).
    *   *Rôle :* Site personnel de l'auteur où il propose de réaliser des audits de sécurité automatisés complets pour des SaaS à partir de 100 $ (rapports au format HTML et Markdown).
*   **Stripe**
    *   *Type :* Service payant (avec commissions par transaction).
    *   *Rôle :* Solution de paiement en ligne utilisée sur le site pour encaisser les paiements des clients souhaitant un audit de leur SaaS.
*   **NoStack**
    *   *Type :* Non précisé (probablement un outil ou une stack technique de développement).
    *   *Rôle :* Utilisé par l'auteur pour créer rapidement le site web de pentest en 10 minutes.

---

### 3. Astuces concrètes et réutilisables

*   **Parallélisation des agents d'IA :** Lancer plusieurs agents en parallèle (par exemple, des dizaines d'agents pendant plusieurs heures) permet d'effectuer un travail d'audit équivalent à des dizaines d'heures de travail humain en un temps record (une nuit).
*   **L'approche "White Hat" (Sécurisée) :** N'utilisez jamais d'agents d'IA ou de scripts d'attaque pour détruire, supprimer ou altérer des données réelles. L'objectif est de trouver les failles et de les corriger, pas de nuire. Si l'agent doit tester la suppression, il doit créer ses propres données et supprimer ses propres données (règle : *supprimer les siennes*).
*   **Les 5 familles de failles critiques à surveiller dans un SaaS :**
    1.  *Secrets et clés exposés* (aucun secret sensible côté client).
    2.  *Autorisation cassée et IDOR* (vérifier l'accès aux objets par identité/rôle à chaque requête).
    3.  *Données ou écritures publiques* (refus par défaut, RLS activé, DTO minimal en sortie).
    4.  *Paiement décidé par le client* (prix et droits dérivés côté serveur, webhooks signés).
    5.  *Injection et exécution de code* (API paramétrées, aucune évaluation dynamique).
*   **Contrôles stricts côté serveur :** Ne jamais faire confiance au client (frontend). Chaque requête doit vérifier *qui* demande *quoi* et si l'utilisateur possède les droits, les rôles et l'abonnement nécessaires.

---

### 4. Chiffres de revenus annoncés (affirmés par l'auteur)

*   **Tarif par audit de SaaS :** 100 $ (pour les 10 premiers rapports).
*   **Paliers tarifaires sur son offre :**
    *   10 premiers rapports : 100 $
    *   10 suivants (rapports 11-20) : 149 $
    *   20 suivants (rapports 21-40) : 199 $
*   **Nombre de clients initiaux :** 4 clients ont déjà rejoint l'offre lors de son lancement (mentionné au moment de la présentation de l'offre).
