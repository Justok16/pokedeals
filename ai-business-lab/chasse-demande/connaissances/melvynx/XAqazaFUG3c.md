# Le SHADCN/UI killer de Cal.com : je te présente COSS UI

Vidéo : https://youtu.be/XAqazaFUG3c · durée 14:05 · résumé Gemini (gemini-3.5-flash, lot de 6) du 2026-10-10
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

**1) L'idée principale**
Présentation de la nouvelle bibliothèque de composants UI React open-source `coss.com/ui` (ou `coss/ui`), conçue par les créateurs de Cal.com. Elle est basée sur `Base UI` (en bêta) au lieu de Radix UI, tout en restant compatible avec l'approche et le CLI de `shadcn/ui`.

**2) Chaque outil, site ou dépôt GitHub cité**
*   **coss.com / coss.com/ui** : Site web et bibliothèque de composants UI pour React/Tailwind. *Gratuit / Open-source.*
*   **Cal.com** : Plateforme de gestion de rendez-vous (entreprise parente derrière coss.com). *Gratuit / Open-source.*
*   **Base UI** (`base-ui.com`) : Bibliothèque de primitives UI non stylisées pour React développée par l'équipe de MUI, Radix et Floating UI. *Gratuit / Open-source (en version bêta).*
*   **Radix UI** : Bibliothèque de primitives UI pour React rachetée par WorkOS. *Gratuit / Open-source.*
*   **WorkOS** : Entreprise ayant racheté Radix UI. *Payant / Offre entreprise.*
*   **shadcn/ui / CLI shadcn** : Outil en ligne de commande pour copier/coller des composants UI dans son projet. *Gratuit / Open-source.*
*   **Tailwind CSS** : Framework CSS utilisé pour le style. *Gratuit / Open-source.*
*   **Next.js** : Framework React utilisé pour la démonstration. *Gratuit / Open-source.*
*   **TanStack Start** : Aperçu brièvement dans l'éditeur. *Gratuit / Open-source.*
*   **Origin UI** (`coss.com origin` / `originui.com`) : Galerie de composants UI prédéfinis. *Gratuit / Open-source.*

**3) Les astuces concrètes et réutilisables**
*   Installer des composants `coss/ui` via le CLI shadcn en pointant directement vers le composant distant (ex : `pnpm dlx shadcn@latest add https://coss.com/ui/...`).
*   Conserver le code directement dans son propre répertoire source pour éviter d'ajouter des couches d'abstraction inutiles.
*   Personnaliser les variables CSS globales (`zinc`, `destructive`, `info`, `warning`, `success`) dans `globals.css` pour adapter le design.
*   Utiliser les blocs "Particles" (composants complexes pré-assemblés comme les boîtes de dialogue ou formulaires) pour construire rapidement des interfaces structurées.

**4) Les chiffres de revenus annoncés**
*   non précisé

---
