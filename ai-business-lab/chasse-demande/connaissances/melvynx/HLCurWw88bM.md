# Je revlève mon MRR après 21 jours de marketing | Lumail to 10k #4

Vidéo : https://youtu.be/HLCurWw88bM · durée 20:14 · résumé Gemini (gemini-3.8-flash) du 2026-09-29
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici la synthèse structurée de la vidéo :

---

### 1) Idée principale
L'auteur présente l'avancement au bout de trois semaines de son SaaS d'emailing orienté agents IA (**Lumail**). Il détaille son modèle économique (tarification hybride abonnement + dépassements à forte marge par rapport au coût d'infrastructure AWS), sa stratégie de protection contre la fraude/phishing via un double pipeline d'agents IA, et l'utilisation de modèles d'IA (famille Claude / Opus) pour coder rapidement des vidéos promotionnelles et des outils web gratuits générateurs de trafic.

---

### 2) Outils, sites et dépôts cités

* **Lumail (lumail.io)** : Plateforme d'emailing conçue pour les agents IA (newsletters, automatisations, transactionnel).  
  * *Modèle :* Gratuit jusqu'à 3 000 emails/mois, puis plans payants (20 $/mois pour Creator, 60 $/mois pour Pro, 200 $/mois pour Business, avec facturation à l'usage excédentaire).
* **Pushrank (pushrank.io)** : Outil d'analyse et de recommandations SEO pour auditer les pages web et détecter des opportunités de mots-clés.  
  * *Modèle :* Non précisé (interface avec crédits visible).
* **Ahrefs SEO Toolbar** : Extension de navigateur pour vérifier l'optimisation technique SEO d'une page.  
  * *Modèle :* Version gratuite / freemium (non précisé).
* **Amazon SES (AWS)** : Infrastructure cloud d'envoi d'emails utilisée en sous-jacent.  
  * *Modèle :* Payant (coût estimé par l'auteur à ~0,20 $ pour 1 000 emails).
* **Jev** : Outil/modèle IA interne à très faible coût servant de premier filtre pour détecter le spam, le phishing et le cold email.  
  * *Modèle :* Non précisé (décrit comme ne coûtant « rien »).
* **Gemini (Google)** : Modèle de langage utilisé comme validateur de second niveau pour confirmer les alertes de Jev et éviter les faux positifs.  
  * *Modèle :* Payant à l'usage de l'API (non précisé).
* **Claude / Opus 5.5** : Modèle d'Anthropic utilisé par l'auteur pour générer le code d'animations vidéo marketing et créer des mini-outils web en une seule invite (*one-shot*).  
  * *Modèle :* Payant (abonnement / API Anthropic).
* **Lumail Mail Tester (lumail.io/tools/mail-tester)** : Outil gratuit pour tester la délivrabilité, les enregistrements DNS (SPF, DKIM, DMARC) et les listes de blocage d'un email.  
  * *Modèle :* Gratuit sans inscription.
* **Lumail Spam Tester (lumail.io/tools/spam-tester)** : Outil gratuit d'analyse sémantique pour détecter les mots déclencheurs de filtres antispam (*trigger words*).  
  * *Modèle :* Gratuit sans inscription.
* **Excalidraw (app.excalidraw.com)** : Application de tableau blanc virtuel utilisée pour structurer la vidéo.  
  * *Modèle :* Gratuit / freemium.
* **X (Twitter)** et **YouTube** : Plateformes de diffusion pour le contenu vidéo, les tests marketing et le podcast (« Le Podcast IA »).  
  * *Modèle :* Gratuit.

---

### 3) Astuces concrètes et réutilisables

1. **Ne pas prioriser le SEO au tout début d'un SaaS :** L'auteur conseille de ne pas perdre de temps sur le référencement naturel en phase de lancement initial (*« Semaine 3 -> ne fait pas SEO »*), car les retombées sont lentes et attirent souvent des spammeurs avant d'attirer des clients qualifiés.
2. **Filtrage anti-abus par IA à deux étages :** 
   * Passer chaque message suspect d'abord par un modèle ultra-économique (Jev).
   * Si classé suspect, faire valider par un LLM plus robuste (Gemini) avant de bloquer le compte, évitant ainsi de payer un grand modèle sur l'ensemble du trafic tout en réduisant les faux positifs.
3. **Ingénierie marketing (*Engineering as Marketing*) :** Utiliser des LLM (comme Claude) pour programmer rapidement des mini-outils gratuits accessibles sans inscription (ex. testeur de spam ou de délivrabilité). Cela attire des liens, améliore le SEO de façon programmatique et sert de passerelle d'acquisition vers le produit payant.
4. **Vidéos marketing codées avec l'IA :** Demander à des modèles avancés de coder directement les animations visuelles et les effets sonores de vidéos de lancement pour les réseaux sociaux en quelques dizaines de minutes.
5. **Tarification à double composante (Forfait + Usage margé) :** Fixer un ticket d'entrée fixe (ex. 20 $/mois) assurant un plancher de revenus, tout en appliquant une forte marge sur les dépassements de volume (ex. coût AWS à 0,20 $/1 000 emails re-facturé 0,70 $/1 000), ce qui pousse naturellement les clients à passer sur des paliers supérieurs plus prévisibles.

---

### 4) Chiffres de revenus annoncés (*affirmé par l'auteur*)

* **MRR actuel :** **520,00 $** (en hausse de +189 % par rapport aux 180,00 $ de la période précédente), avec **22 clients payants** (*affirmé par l'auteur*).
* **Revenu réel avec dépassements d'usage :** supérieur au MRR affiché ; exemple d'un utilisateur sur le plan de base à 20 $/mois ayant été facturé **80 $** sur un mois en raison de ses volumes d'envois (*affirmé par l'auteur*).
* **Objectif financier affiché :** Atteindre **10 000 $ de MRR** (multiplier par 20 le palier des 500 $) (*affirmé par l'auteur*).
* **Volume total d'emails traités :** **4 709 597 emails** envoyés (dont 109 700 sur les 7 derniers jours) (*affirmé par l'auteur*).
