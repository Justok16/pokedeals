# Chrome supporte le "Squircle" je t'explique tout

Vidéo : https://youtu.be/2d0vKEo0jM8 · durée 9:13 · résumé Gemini (gemini-3.5-flash-lite, lot de 6) du 2026-10-08
(connaissances générales, non vérifiées : toute règle fiscale ou chiffre est à contrôler à la source officielle)

1) **Idée principale :** Découverte et tutoriel d'utilisation des **Corner Shapes** (les nouvelles propriétés CSS pour créer des formes de coins avancées comme le style iOS, incluant *squircle*, *superellipse*, *notch*, *bevel*, etc.), avec une démonstration de leur intégration via Tailwind CSS grâce au plugin `tailwind-corner-shape`.

3) **Astuces concrètes et réutilisables :**
- Utiliser la propriété CSS `corner-shape` (associée à `border-radius`) pour reproduire le lissage de coins caractéristique d'iOS (style *squircle* ou *superellipse*) directement en code natif, évitant ainsi d'avoir recours à des masques d'images complexes.
- Installer et configurer le plugin Tailwind tiers `tailwind-corner-shape` via npm (`pnpx pnpm install tailwind-corner-shape` puis en l'important dans `globals.css`) pour appliquer rapidement des classes utilitaires de formes de coins (`corner-squircle`, `corner-notch`, etc.) sur n'importe quel élément HTML.
- Connaître les limites de compatibilité des navigateurs actuels : les *corner shapes* et superellipses sont principalement supportées sur les navigateurs basés sur Chromium (Chrome, Edge), mais nécessitent encore des précautions ou ne sont pas pleinement prises en charge sur Safari iOS ou certains environnements mobiles.

4) **Chiffres de revenus annoncés :**
- Non précisé (aucun chiffre de revenus, de gains ou de prix n'est mentionné dans ce tutoriel CSS).

---
