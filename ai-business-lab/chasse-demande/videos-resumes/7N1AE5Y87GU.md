# 7N1AE5Y87GU — « I Stopped Using Google Docs. Claude Artifacts Do Everything Now »

- Auteur : Riley Brown ; lien : https://youtu.be/7N1AE5Y87GU
- Envoyée par l'utilisateur ; résumée le 19/11/2026 par Gemini (via le relais, modèle gemini-3.8-flash)
- Les chiffres ci-dessous sont « affirmés par l'auteur », non vérifiés.

## Tri pour DIG16 (19/11)

- **Utile pour DIG16** : un artefact « Design System » qui fixe la charte DIG16 (polices, couleurs, espacements) pour que les visuels faits par Claude restent cohérents. Notre charte existe déjà en fichiers (`60-charte-dig16.md`, `outils/marque/`) et sert à toutes nos images : rien à refaire tant que tout passe par nos scripts. En réserve : à créer au premier client, pour décliner sa propre charte (site, cartes, réseaux).
- **Déjà en place** : pilotage à distance depuis le téléphone (cette conversation en est un), commentaires sur image pour corriger un visuel (fait avec tes captures).
- **Écarté** : « artefact → appli web avec GitHub + Convex + Vercel » (nos sites sont statiques, Cloudflare Pages gratuit suffit) ; Revolut Business (segment sponsorisé, rien à voir avec un besoin actuel) ; Final Draft et les démos de jeu ; « Claude Motion / Dashboards » (réservés aux offres Team selon l'auteur). v2.video déjà en réserve (11/11).

## Résumé (Gemini)

Voici le résumé structuré de la vidéo :

---

### 1) Idée principale
L'auteur explique pourquoi **Claude Code** et l'écosystème d'**Artifacts d'Anthropic** représentent selon lui la plateforme d'agents IA la plus puissante pour le travail et le business. Grâce aux 7 types d'artefacts (documents, feuilles de calcul, diapositives, designs, systèmes de design, données, tableaux blancs), à l'accès direct aux fichiers de l'ordinateur et à la compréhension visuelle des modèles (comme Opus 5.5), il est désormais possible de concevoir, prototyper et déployer des applications web ou des outils internes complets en quelques prompts, sans barrière technique.

---

### 2) Outils, sites et dépôts cités

1. **Claude Code / Claude (Anthropic)**
   * **Statut :** Gratuit / Payant (accès avancé et modèles Opus 5.5 / Fable 5.2 soumis aux abonnements Pro/Team et limites de tokens).
   * **Utilité :** Environnement d'agent IA interactif capable d'agir sur l'ordinateur, d'exécuter du code, d'éditer des fichiers et de générer 7 types d'artefacts visuels et interactifs.

2. **GitHub**
   * **Statut :** Gratuit pour démarrer (freemium).
   * **Utilité :** Hébergement de dépôts de code source pour versionner et stocker les projets créés par Claude.

3. **Vercel**
   * **Statut :** Gratuit pour démarrer (freemium).
   * **Utilité :** Hébergement et déploiement instantané d'applications web frontend générées par Claude.

4. **Convex**
   * **Statut :** Gratuit pour démarrer (freemium).
   * **Utilité :** Backend réactif et base de données cloud connecté aux applications créées avec Claude.

5. **Revolut Business** *(Sponsor du segment)*
   * **Statut :** Formules gratuites et payantes (*non précisé* en détail).
   * **Utilité :** Compte professionnel pour gérer la trésorerie d'entreprise, les virements internationaux multi-devises et l'émission de cartes virtuelles avec plafonds de dépenses.

6. **MCP (Model Context Protocol)**
   * **Statut :** Gratuit / Open source.
   * **Utilité :** Protocole d'Anthropic permettant de connecter un agent IA à des API et outils externes (ex. création d'un serveur MCP Revolut pour préparer des paiements ou consulter les soldes).

7. **v2.video**
   * **Statut :** *Non précisé*.
   * **Utilité :** Présenté comme le « GitHub du montage vidéo » pour stocker, prévisualiser et partager des fichiers vidéo et animations avec son équipe.

8. **Final Draft**
   * **Statut :** Payant (199,99 $/an ou abonnement mensuel).
   * **Utilité :** Logiciel de référence pour l'écriture de scénarios hollywoodiens (l'auteur s'en sert d'exemple pour montrer comment cloner ses fonctionnalités clés dans sa propre web app).

9. **Claude Motion / Claude Dashboards**
   * **Statut :** Payant / Bêta réservée aux forfaits Team de Claude (*non précisé* pour le grand public).
   * **Utilité :** Transformation de tableaux de bord et données en animations vidéos 3D interactives.

10. **Saltline**
    * **Statut :** Démo / *Non précisé*.
    * **Utilité :** Jeu vidéo 3D jouable directement à l'intérieur d'un artefact Claude, créé par Felix d'Anthropic en un prompt.

11. **Autres connecteurs/outils montrés à l'écran :**
    * *Google Drive, Google Calendar, Gmail, ClickUp, Descript, Slack* : intégrations tierces pour alimenter l'agent en données contextuelles.

---

### 3) Astuces concrètes et réutilisables

* **La formule « Artefact $\rightarrow$ Web App » en 3 étapes :** Demandez à Claude de créer un artefact fonctionnel, puis invitez-le à le transformer en application complète en intégrant la stack gratuite **GitHub + Convex (base de données) + Vercel (hébergement)**.
* **Commentaires directs pour le design :** Dans les artefacts de type *Design* ou *Docs*, cliquez directement sur un élément visuel ou du texte pour laisser un commentaire (ex. `@Claude change cette couleur` ou `refais cette illustration`), ce qui réinjecte une consigne précise à l'agent sans reformuler tout le contexte.
* **Automatiser les visuels de contenu :** Vous pouvez rédiger une newsletter ou un article dans un artefact *Docs*, demander à Claude de concevoir des schémas explicatifs dans un artefact *Design* jumeau, puis lui faire insérer les images exportées directement dans le texte final.
* **Mode « Bypass permissions » de Claude Code :** Permet à l'agent d'analyser en profondeur le disque dur local (espace disque, gros fichiers vidéo, caches de développement) et de synthétiser les résultats sous forme de graphiques camembert ou de diagrammes de Gantt interactifs.
* **Garder une charte graphique cohérente :** Créez un artefact *Design System* (typographie, palette de couleurs, espacements) et demandez à Claude de baser toutes ses créations ultérieures (slides, pages web, graphiques) sur ce système.
* **Contrôle à distance (Claude Remote) :** Configurez Claude Remote pour piloter vos sessions Claude Code et lancer des tâches d'agent directement depuis votre smartphone.

---

### 4) Chiffres de revenus et montants annoncés

* **Bonus de parrainage Revolut Business :** **200 $** de bonus offerts à l'ouverture d'un nouveau compte professionnel après un dépôt initial d'au moins **0,01 $** *(affirmé par l'auteur / offre sponsorisée)*.
* **Coût du logiciel Final Draft :** **199,99 $/an** ou abonnement mensuel *(affirmé par l'auteur)*.
* **Chiffres d'affaires et pipelines affichés à l'écran :** Plusieurs montants apparaissent sur les tableaux de bord présentés (ex. **208 000 $**, **232 000 $**, **389 600 $**), mais l'auteur précise explicitement qu'il s'agit de **données fictives** pour une entreprise fictive nommée *« Halyard Agent Works »*.
* **Gain potentiel du contenu IA :** L'auteur affirme de manière générale que ceux qui réussiront à automatiser la production de contenu à grande échelle avec l'IA « gagneront des millions » *(affirmé par l'auteur, aucune preuve ni revenu personnel divulgué)*.
