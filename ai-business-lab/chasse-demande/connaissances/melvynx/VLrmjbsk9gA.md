# Les NOUVEAUX composants Shadcn/UI révélés : premier test

Vidéo : https://youtu.be/VLrmjbsk9gA · durée 25:10 · résumé Gemini (gemini-flash-lite-latest, lot de 6) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale**
Présentation et intégration des nouveaux composants de la bibliothèque **shadcn/ui** (Button Group, Input Group, Empty State, Item and Item Group, Field, etc.) dans une application SaaS.

2) **Outils, sites ou dépôts GitHub cités**
* **shadcn/ui** : Bibliothèque de composants open source gratuite.
* **Tailwind CSS** : Framework CSS utilisé pour le design.
* **React Hook Form** : Librairie de gestion de formulaires React.
* **Zod** : Librairie de validation de schémas.

3) **Astuces concrètes et réutilisables**
* **Button Group** : Grouper plusieurs boutons ensemble (pour la pagination, les actions groupées) en wrappant les composants `Button` dans un conteneur `<ButtonGroup>`.
* **Input Group** : Combiner des inputs avec des icônes, des boutons, des sélecteurs ou des addons textuels (comme des boutons de recherche ou des préfixes) en utilisant `<InputGroup>`, `<InputGroupAddon>`, etc.
* **Empty State** : Utiliser le composant `<Empty>` (ou `EmptyState`) pour afficher des états vides propres (lorsqu'il n'y a pas de données, de abonnés ou de workflows), incluant icône, titre, description et bouton d'action.
* **Field (React Hook Form)** : Utiliser le composant `Field` pour créer des formulaires complexes de manière unifiée, en évitant d'importer séparément tous les sous-composants de labels et d'erreurs.
* **Item et Item Group** : Créer des conteneurs flexibles de type liste ou carte pour afficher des éléments avec avatar, titre, description, liens et boutons d'actions alignés (idéal pour les listes d'e-mails ou de profils).

4) **Chiffres de revenus annoncés (affirmés par l'auteur)**
* Non précisé

---
