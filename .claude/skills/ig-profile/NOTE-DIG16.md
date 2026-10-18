# Note DIG16 (18/10/2026)

Source : https://github.com/Jakeschincariol/instagram-agent-skill (MIT, commit d03c56b, lu en entier, aucun accès réseau).
Seuls `ig-caption` et `ig-profile` sont installés. Textes DIG16 en français :
- le contrôle « ONE ASK » ne reconnaît que des appels à l'action en anglais : le juger à l'œil ;
- `ig-human` / `humanize.py` n'est **pas** installé : il remplace l'apostrophe ’ et les espaces insécables, ce qui casse la
  typographie française exigée (`connaissances/lecons.md`).
Usage : `python3 -I .claude/skills/ig-caption/caption.py legende.txt --keywords "site internet,artisan"`.
