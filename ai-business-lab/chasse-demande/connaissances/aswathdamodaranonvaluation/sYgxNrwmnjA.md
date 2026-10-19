# Séance 4 (Étudiants en premier cycle en évaluation) : L'architecture des DCF et des taux sans risque

Vidéo : https://youtu.be/sYgxNrwmnjA · durée 1:01:29 · résumé Gemini (gemini-3.1-flash-lite) du 2026-10-19
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

Voici une fiche de connaissances basée sur la présentation d'Aswath Damodaran, professeur de finance à la Stern School of Business de NYU.

---

### **Fiche de connaissances : La méthode DCF (Discounted Cash Flow)**

#### **1) Sujet et thèse principale**
*   **Sujet :** L'évaluation d'entreprise par la méthode des flux de trésorerie actualisés (DCF).
*   **Thèse principale :** Pour valoriser correctement une entreprise, il est crucial d'appliquer le "principe de cohérence" (*Discounting Consistency Principle*) : le taux d'actualisation doit impérativement correspondre à la nature des flux de trésorerie projetés (ex : flux vers les capitaux propres vs flux vers l'entreprise entière). Le non-respect de cette règle conduit à des erreurs majeures d'évaluation.

#### **2) Notions expliquées**
*   **DCF (Discounted Cash Flow) :** Méthode visant à déterminer la valeur d'une entreprise en actualisant ses futurs flux de trésorerie attendus.
*   **Principe de cohérence :** Si les flux sont calculés après paiement de la dette (destinés aux actionnaires), on utilise le coût des capitaux propres. Si les flux sont calculés avant paiement de la dette, on utilise le coût moyen pondéré du capital (WACC).
*   **Effet d'incohérence (Mismatch Effect) :** Erreur consistant à mélanger des types de flux et des taux d'actualisation incompatibles, ce qui fausse totalement le résultat.
*   **Risque dans le DCF :** Le risque ne doit être intégré qu'à un seul endroit : le taux d'actualisation. "Double compter" le risque en réduisant les prévisions de flux *et* en augmentant le taux d'actualisation est une erreur courante.
*   **Taux sans risque :** La base de tout calcul de coût du capital. Il doit être monétaire (ex: taux des obligations d'État) et correspondre à la monnaie dans laquelle les flux sont prévus.

#### **3) Chiffres, taux et règles cités**
*   **Exemple chiffré :** L'auteur illustre le calcul avec un taux de coût des capitaux propres de 13,625 % et un coût de la dette avant impôt de 10 % (avec un taux d'imposition de 50 %, soit 5 % après impôt).
*   **Règle de base (Taux sans risque) :** Utiliser le taux des obligations d'État à 10 ans est une pratique courante par commodité, bien que les obligations à 30 ans soient théoriquement plus proches de la durée de vie des flux.
*   **Règle (Dette sans intérêt) :** Les dettes qui ne portent pas d'intérêts (comptes fournisseurs) ne doivent pas être soustraites dans le calcul pour passer de la valeur de l'entreprise à la valeur des capitaux propres.
*   **Règle (Inflation) :** Un taux d'actualisation doit être "nominal" si les flux sont "nominaux" (incluant l'inflation).
*   *Note : Toutes ces règles financières sont des pratiques académiques de valorisation ; elles doivent être vérifiées à la source officielle pour tout usage fiscal ou comptable légal.*

#### **4) Conseils concrets, limites et risques**
*   **Conseil :** Toujours commencer par étudier le passé (l'historique financier) pour comprendre la structure de l'entreprise avant de projeter le futur, sans pour autant le copier servilement.
*   **Limite :** Les modèles de valorisation sont toujours basés sur des hypothèses. Le risque est omniprésent, mais une grande partie du risque (risque macroéconomique) ne peut pas être diversifiée.
*   **Risque :** Se focaliser uniquement sur les données comptables sans comprendre la stratégie (croissance, marges, besoin en réinvestissement).
*   **Attention :** Le risque lié au défaut de paiement d'un État (ex: Argentine) doit être déduit du taux sans risque si l'on travaille dans une monnaie locale risquée.

#### **5) Produits, entreprises et applications cités**
*   **Tesla, Alibaba, Kraft Heinz, Google, Apple :** Utilisés uniquement comme exemples d'entreprises pour illustrer les concepts de valorisation.
*   **Bloomberg :** Cité comme source de données financières pour les analystes.
*   **Moody's :** Cité comme agence de notation pour évaluer le risque de défaut des pays.
*   *Note : Il ne s'agit pas de publicités, mais d'exemples d'outils et de cas réels utilisés dans la pratique professionnelle de la finance.*
