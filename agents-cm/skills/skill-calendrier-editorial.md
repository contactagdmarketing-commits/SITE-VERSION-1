# SKILL : Calendrier Éditorial — Candidalib

Ce skill guide la création du calendrier éditorial mensuel pour Candidalib.
Toujours lire skill-candidalib.md avant d'appliquer ce skill.

---

## Fréquence par réseau

| Réseau | Fréquence | Meilleur moment |
|---|---|---|
| Instagram | 4-5 posts/semaine + stories quotidiennes | Lundi-vendredi 7h-9h ou 18h-20h |
| Facebook | 3-4 posts/semaine | Mardi-jeudi 12h-14h |
| TikTok | 3-5 vidéos/semaine | 18h-22h tous les jours |
| Google Business | 2 posts/semaine | N'importe quand (algo non horaire) |

---

## Saisonnalité Candidalib

### Périodes CHAUDES (forte demande)
- **Janvier-Février** : bonnes résolutions, nombreux candidats qui se lancent
- **Avril-Juin** : pic avant les vacances d'été, tout le monde veut son permis pour l'été
- **Août-Septembre** : rentrée, nouveaux candidats, étudiants qui arrivent à Toulouse
- **Novembre** : préparation pour avant les fêtes

### Périodes CREUSES (fidélisation + contenu éducatif)
- **Juillet** : vacances, moins de candidats actifs → contenu evergreen, témoignages
- **Décembre** : fêtes → contenu léger, bilan annuel, voeux

---

## Modèle de calendrier mensuel (4 semaines)

### Semaine 1 — Éducation + Lancement
| Jour | Réseau | Thème | Format |
|---|---|---|---|
| Lundi | Instagram + Facebook | Pilier Éducation : "Comment passer le permis en candidat libre" | Carrousel + Post |
| Mardi | TikTok | "Tu savais que tu pouvais passer ton permis sans auto-école ?" | Script vidéo |
| Mercredi | Google Business | Post informatif avec mots-clés locaux | Post |
| Jeudi | Instagram | Coulisses : présentation du véhicule / accompagnateur | Post photo |
| Vendredi | Facebook | FAQ : questions fréquentes candidats libres | Post texte |

### Semaine 2 — Preuve sociale
| Jour | Réseau | Thème | Format |
|---|---|---|---|
| Lundi | Instagram | Témoignage client (texte + visuel) | Post |
| Mardi | TikTok | "Ce que personne te dit sur le permis en candidat libre" | Script vidéo |
| Mercredi | Google Business | Post avec mention des villes desservies | Post |
| Jeudi | Instagram + Facebook | Avis Google mis en avant | Post |
| Samedi | Instagram | Contenu inspirationnel : "Ton permis, ton indépendance" | Story + Post |

### Semaine 3 — Démystification
| Jour | Réseau | Thème | Format |
|---|---|---|---|
| Lundi | Instagram | "Candidat libre vs auto-école : le vrai comparatif" | Carrousel |
| Mardi | TikTok | Mythe démystifié : "C'est pas légal" → on répond | Script vidéo |
| Mercredi | Google Business | Post focalisé sur un lieu d'examen (ex: Colomiers) | Post |
| Jeudi | Facebook | Contenu parents : "Votre enfant candidat libre, comment ça marche ?" | Post |
| Vendredi | Instagram | "Les 5 erreurs à éviter en candidat libre" | Carrousel |

### Semaine 4 — Conversion
| Jour | Réseau | Thème | Format |
|---|---|---|---|
| Lundi | Instagram + Facebook | Post tarifs + CTA direct | Post |
| Mardi | TikTok | "Voilà ce que tu as pour 45€/h avec Candidalib" | Script vidéo |
| Mercredi | Google Business | Post offre + numéro de téléphone | Post |
| Jeudi | Instagram | Urgence douce : "Les places partent vite avant [saison]" | Story + Post |
| Vendredi | Facebook | Récapitulatif : tout ce que Candidalib peut faire pour toi | Post |

---

## Variables saisonnières à injecter

Le calendrier doit adapter ces éléments selon le mois :
- **Janvier** : "Nouvelle année, nouveau permis ?"
- **Avril** : "L'été arrive — t'as pensé à ton permis ?"
- **Août** : "Rentrée = nouveau départ. Et si c'était l'année du permis ?"
- **Avant les vacances scolaires** : "Profite des vacances pour avancer sur ton permis"

---

## Instructions pour l'Agent Stratège

Quand tu génères un calendrier :
1. Demande le mois cible et les événements spéciaux prévus
2. Applique la saisonnalité Candidalib
3. Respecte l'alternance des 4 piliers (Éducation 40% / Preuve sociale 25% / Coulisses 20% / Offre 15%)
4. Produis le calendrier en tableau Markdown avec : Jour | Réseau | Thème | Format | Accroche suggérée
5. Pour chaque post, indique le pilier éditorial correspondant

---

## Convention de nommage — Images et fichiers texte

**Règle absolue : le nom de l'image et l'intitulé de la section dans le draft doivent inclure le jour ET la date précise.**

### Format du nom
```
[jour]-[date]-[mois]-[réseau].jpg
[jour]-[date]-[mois]-[réseau]-[type].jpg   ← si plusieurs posts le même jour sur le même réseau
```

### Exemples
| Image | Section dans le draft |
|---|---|
| `lundi-29-juin-instagram.jpg` | `## LUNDI 29 JUIN — Instagram` |
| `jeudi-2-juillet-instagram.jpg` | `## JEUDI 2 JUILLET — Instagram` |
| `vendredi-3-juillet-facebook.jpg` | `## VENDREDI 3 JUILLET — Facebook` |
| `samedi-4-juillet-instagram-story.jpg` | `## SAMEDI 4 JUILLET — Instagram Story` |
| `mardi-30-juin-tiktok.jpg` | `## MARDI 30 JUIN — TikTok` |
| `mercredi-1-juillet-google-business.jpg` | `## MERCREDI 1 JUILLET — Google Business` |

### Réseaux acceptés dans les noms
- `instagram`
- `facebook`
- `tiktok`
- `google-business`

### Règles
- Tout en minuscules
- Pas d'espaces — utiliser des tirets `-`
- La date précise est OBLIGATOIRE dans le nom (ex: `29-juin`, `3-juillet`)
- Le fichier draft suit le format : `semaine[N]-[mois][année].md` (ex: `semaine1-juillet2026.md`)
- Les images vont dans `outputs/images/[mois][année]/semaine[N]/`
- Les drafts vont dans `outputs/drafts/`
