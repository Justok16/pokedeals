# La PIRE Erreur de useState en React 🤯

Vidéo : https://youtu.be/Qyx0ZNUwcnc · durée 8:28 · résumé Gemini (gemini-flash-lite-latest, lot de 4) du 2026-10-04
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :**  
Éviter l'erreur du « derived state » (état dérivé) dans React, qui consiste à dupliquer des données issues d'une source unique de vérité, entraînant des incohérences d'affichage.

2) **Outils, sites ou dépôts GitHub cités :**  
- **React** (gratuit, framework/bibliothèque UI) — non mentionné comme payant.  
- **Vite** (gratuit, outil de build) — mentionné visuellement.  
- **VS Code** (gratuit, éditeur de code) — mentionné visuellement.  
- **BeginReact.dev** (payant, plateforme de formation / masterclass) — sert à se former sur React/JSX/ReactDOM.  

3) **Astuces concrètes et réutilisables :**  
- Ne conserver qu'une **seule source de vérité** pour chaque donnée.  
- Au lieu de stocker un objet complet dans le state (ex. `selectedBook`), stocker uniquement son identifiant (ex. `selectedBookId`) et le retrouver dynamiquement (avec `.find()`) pour éviter les désynchronisations lors des mises à jour.  

4) **Chiffres de revenus annoncés :**  
- Non précisé (la vidéo ne traite pas de monétisation d'application).

---
