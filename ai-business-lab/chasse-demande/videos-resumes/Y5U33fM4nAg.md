# Y5U33fM4nAg — « How to Edit Video Ads With AI (Step by Step with Claude Code) »

- Auteur : Mr. Paid Social ; lien : https://youtu.be/Y5U33fM4nAg
- Envoyée par l'utilisateur ; résumée le 17/11/2026 par Gemini (via le relais, modèle gemini-3.5-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (17/11)

- **Même usage que vAxfs4l0-oQ** (montage d'une vidéo filmée par un agent Claude Code : coupes, sous-titres avec Whisper, habillage animé).
- **Vérifié à la source le 17/11** : dépôt `mrpaidsocial/mrpaidsocial-video-editor-agent` : **aucune licence** déclarée (donc tous droits réservés) : on peut s'en inspirer, pas recopier son code.
- **Idée intéressante, mise en réserve** : une page de relecture où l'on clique sur la vidéo pour laisser un commentaire horodaté que l'agent lit et applique (service here.now, offre gratuite annoncée par l'auteur, à vérifier à la source le jour venu). Pour DIG16, l'équivalent utile serait une **page de relecture de site pour le client** (il clique sur un endroit du site et écrit sa remarque) : à ressortir au premier site client livré, en comparant avec nos captures annotées.

## Résumé (Gemini)

Voici le résumé détaillé de la vidéo, structuré selon vos exigences :

---

### 1) Idée principale
L'auteur (Caleb Kruse, alias *Mr. Paid Social*) explique comment créer et automatiser un **agent de montage vidéo IA** basé sur **Claude Code** (ou Codex). Ce système permet de prendre une simple vidéo brute (un enregistrement face caméra ou un script vocal) et de laisser l'agent IA gérer l'intégralité du montage : création du B-roll, sous-titrage automatique sans fautes, ajouts de motion graphics, découpage dynamique et intégration des retours clients. L'objectif est de produire des publicités vidéo à fort taux de conversion pour des plateformes comme Meta, TikTok ou Snapchat, de manière 100 % légale et sans avoir à embaucher une équipe de monteurs.

---

### 2) Outils, sites et dépôts GitHub cités

*   **Claude Code / Claude (Anthropic)**
    *   *Statut :* Payant (via abonnement / API).
    *   *Utilité :* Agent IA principal qui exécute les scripts de montage, analyse le code, génère la structure de la vidéo et applique les consignes de retours.
*   **OpenAI Codex**
    *   *Statut :* Payant (via API).
    *   *Utilité :* Cité comme alternative à Claude Code pour exécuter l'agent de montage IA.
*   **Dépôt GitHub : `video-editor-agent`**
    *   *Statut :* Gratuit / Open Source.
    *   *Utilité :* Dépôt public créé par l'auteur contenant l'ensemble des compétences (*skills*), scripts et instructions pour configurer l'agent de montage vidéo IA.
*   **Here.now (`here.now`)**
    *   *Statut :* Gratuit (Offre gratuite : 500+ sites, 10 Go de stockage) / Payant (Options Hobbyste à 4 $/mois et Développeur à 20 $/mois).
    *   *Utilité :* Plateforme web de révision vidéo interactive. Elle génère une page où l'on peut ajouter des commentaires horodatés. L'agent IA est connecté à cette page et lit directement les commentaires pour effectuer les corrections sur le montage.
*   **Frame.io**
    *   *Statut :* Payant (Freemium).
    *   *Utilité :* Cité à titre de comparaison pour expliquer le fonctionnement du canevas de révision de Here.now.
*   **FFmpeg**
    *   *Statut :* Gratuit / Open Source.
    *   *Utilité :* Logiciel en ligne de commande utilisé localement par l'agent IA pour découper, assembler et restituer les fichiers vidéo/audio.
*   **HyperFrames**
    *   *Statut :* Non précisé dans la vidéo.
    *   *Utilité :* Outil/bibliothèque permettant de générer automatiquement des éléments graphiques en mouvement (motion graphics), des sous-titres stylisés et des mises en page d'écran.
*   **Whisper (OpenAI / Wispr)**
    *   *Statut :* Gratuit / Open Source.
    *   *Utilité :* Outil de transcription audio-vers-texte pour générer des sous-titres ultra-précis et synchroniser les coupes sur la parole.
*   **Gemini API (Google)**
    *   *Statut :* Gratuit / Payant (via API).
    *   *Utilité :* Utilisé comme couche d'auto-évaluation (QA visual reviewer). L'agent envoie les rendus vidéo à Gemini qui "regarde" la vidéo, vérifie le rythme et la qualité visuelle, puis renvoie ses remarques à Claude Code pour correction avant validation par un humain.
*   **Playwright**
    *   *Statut :* Gratuit / Open Source.
    *   *Utilité :* Outil d'automatisation de navigateur utilisé par l'agent IA pour effectuer des captures et enregistrements d'écran automatiques sur des sites web.
*   **Screen Studio**
    *   *Statut :* Payant.
    *   *Utilité :* Outil d'enregistrement d'écran utilisé pour enregistrer les démonstrations d'interface et le B-roll.
*   **Suno**
    *   *Statut :* Gratuit / Payant.
    *   *Utilité :* Générateur de musique par IA utilisé pour créer des pistes sonores/chansons originales adaptées aux publicités.
*   **Arcads**
    *   *Statut :* Payant.
    *   *Utilité :* Cité pour l'explication des workflows d'annonces avec des déclinaisons d'accroches (*hooks*).
*   **Avail / CreatorAPI (`creatorapi.ai`)**
    *   *Statut :* Payant (Sponsor de la vidéo).
    *   *Utilité :* Plateforme qui connecte les marques et les créateurs de contenu. Elle permet aux marques de licencier légalement l'image/voix d'un créateur pour générer des dizaines de variations vidéo par IA, tout en garantissant que le créateur valide chaque variante et soit rémunéré.
*   **Skool ("The AI Ads Alchemists")**
    *   *Statut :* Payant (97 $/mois).
    *   *Utilité :* Communauté privée de l'auteur regroupant des créateurs et des agences pour partager les templates et workflows automatisés d'annonces IA.

---

### 3) Astuces concrètes et réutilisables

1.  **Méthode du "Foundational Clip" (Clip de base) :**
    *   Enregistrez simplement un fichier vidéo brut (ex: depuis votre smartphone ou caméra) en lisant votre script. Ne perdez pas de temps à faire du montage manuel. L'IA se sert de la piste audio et de la transcription comme colonne vertébrale du projet.
2.  **Consignes visuelles intégrées dans le script :**
    *   Ajoutez des indications visuelles entre crochets directement dans le fichier texte du script (ex: `[écran montrant l'annonce Capital One]`). L'agent IA lira ces balises pour savoir précisément quand et quel B-roll capturer ou générer.
3.  **Boucle de révision IA à IA (Claude + Gemini) :**
    *   Configurez votre agent pour qu'il envoie ses rendus intermédiaires à l'API Gemini. Comme Gemini est très performant pour l'analyse vidéo, il donne un premier retour technique à Claude Code qui corrige les erreurs avant même que vous n'ayez à regarder la vidéo.
4.  **Journal de mémoire (`SESSION_LOG.md`) :**
    *   Demandez à l'agent IA de créer un fichier journal de session après chaque projet. L'IA y consigne ce qui a fonctionné, ce qui a échoué et la charte graphique du client. Les sessions futures liront ce fichier pour ne pas répéter les mêmes erreurs et économiser des jetons API.
5.  **Gestion fluide des retours clients via Here.now :**
    *   Partagez le lien du canevas de révision Here.now avec votre client. Le client laisse ses remarques aux horodatages souhaités. Il vous suffit ensuite d'envoyer le lien à Claude Code pour qu'il génère la version V2 automatiquement.

---

### 4) Chiffres de revenus annoncés (*affirmé par l'auteur*)

*   **Chiffre d'affaires mensuel :** L'auteur affirme que ce système d'agent IA de montage vidéo a propulsé son activité à plus de **100 000 $ / mois** (captures d'écran affichant des totaux de **100 828 $** et **110 327 $** de revenus mensuels).
*   **Tarif de sa communauté Skool :** **97 $ / mois**.
