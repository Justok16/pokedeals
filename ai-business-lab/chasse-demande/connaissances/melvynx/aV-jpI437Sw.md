# Nouveau : Shadcn/UI ajoute les SideBar : C'EST cheaté.

Vidéo : https://youtu.be/aV-jpI437Sw · durée 25:48 · résumé Gemini (gemini-flash-lite-latest, lot de 7) du 2026-10-15
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Découverte et intégration pas à pas de nouveaux composants « Sidebar » de Shadcn UI dans une application existante, en montrant comment structurer, thématiser et personnaliser ces barres latérales.

2) **Outils, sites ou dépôts GitHub cités :**
- **Shadcn UI** (ou shadcn/ui) : Site web / librairie open-source gratuite de composants UI.
- **npm / npx** : Outil en ligne de commande pour installer des paquets.
- **VS Code (Visual Studio Code)** : Éditeur de code (logiciel).
- **Not (ou NotTS / NextJS / Vite / Laravel)** : Frameworks ou environnements mentionnés comme compatibles.
- **Lucide React** : Librairie d'icônes open-source gratuite (utilisée pour les icônes des menus).

3) **Astuces concrètes et réutilisables :**
- Utiliser la commande `npx shadcn@latest add sidebar` pour installer le composant sidebar.
- Gérer l'état d'ouverture/fermeture et la réactivité mobile grâce au hook `useSidebar` et au composant `SidebarProvider`.
- Personnaliser le style des barres latérales via les variables CSS globales (`globals.scss` ou équivalent) et les classes Tailwind.
- Structurer la sidebar avec des blocs sémantiques : `SidebarHeader`, `SidebarContent`, `SidebarGroup`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton` et `SidebarTrigger`.
- Configurer des sous-menus rétractables (*collapsible*) et utiliser des raccourcis clavier (par exemple, la touche « b ») pour basculer l'affichage de la sidebar.
- Utiliser les variantes de positionnement (`side="left" | "right"`, `variant="floating" | "inset"`).

4) **Chiffres de revenus annoncés :**
- Non précisé.
